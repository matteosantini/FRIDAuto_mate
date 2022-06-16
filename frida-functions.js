// Returns the list [id] -> activity_name
function enumerateActivities(package_name){
  Java.perform(function(){
  var rclass = Java.use(`${package_name}.R$layout`);//
  var arr = Object.keys(rclass);
  console.log("*********************************");
  console.log("[index] => activity");
  var idx = 0;
  for (var i = 0; i < arr.length; i++) {
    if(arr[i].includes("activity")){
      console.log("["+ idx++ +"] => " + arr[i]);
    }
   }
  console.log("*********************************");
  })
}

//takes the activity index from python, it hooks onStart executing setContentView()
function goToActivity(package_name, idx_py){
  Java.perform(function (){
      var appCompatActivity = Java.use('androidx.appcompat.app.AppCompatActivity');
      var rclass = Java.use(`${package_name}.R$layout`);

      appCompatActivity.onStart.overload().implementation = function () {
        // Loads array [idx] -> R.layout.id
        var rclass = Java.use(`${package_name}.R$layout`);
        var arr = Object.keys(rclass);
        var loaded_activities = [];
        var idx = 0;
        for (var i = 0; i < arr.length; i++) {
          if(arr[i].includes("activity")){
            loaded_activities[idx++] = rclass[arr[i]].value; // idx -> R.layout.id
          }
         }
        this.setContentView(loaded_activities[idx_py]);
        var ret = this.onStart();
      };
  })
}

//enumerate apk loaded classes. // TODO: insert find functionality
function enumerateApplicationClasses(search_keyword){//class_name = null){
  Java.perform(function() {
      Java.enumerateLoadedClasses({
          onMatch: function(className) {
               if(className.includes(search_keyword)){
                  console.log(`[CLASS] ${className}`);
               }
          },
          onComplete: function() {}
      });
  });
}

//intercept sql queries
function interceptSQLiteQueries(){
  Interceptor.attach(Module.findExportByName('libsqlite.so', 'sqlite3_prepare16_v2'), {
        onEnter: function(args) {
            console.log('[DB] ' + Memory.readUtf16String(args[0]) + '\tSQL: ' + Memory.readUtf16String(args[1]));
        }
  });
  console.log("[*] SQL Query interceptor activated");
}

function printRunTimeStrings(){
  Java.perform(function() {
    ['java.lang.StringBuilder', 'java.lang.StringBuffer'].forEach(function(clazz, i) {
      console.log('[?] ' + i + ' = ' + clazz);
      var func = 'toString';
      Java.use(clazz)[func].implementation = function() {
        var ret = this[func]();
        if (ret.indexOf('') != -1) {
          // print stacktrace if return value contains specific string
          Java.perform(function() {
            var jAndroidLog = Java.use("android.util.Log"), jException = Java.use("java.lang.Exception");
            console.log( jAndroidLog.getStackTraceString( jException.$new() ) );
          });
        }
        send('[' + i + '] ' + ret);
        return ret;
      }
    });
  });
}

function changeLocation(latitude_inp, longitude_inp){
  Java.perform(() => {
  	var Location = Java.use('android.location.Location');
  	Location.getLatitude.implementation = function() {
      var latitude = parseFloat(latitude_inp)
  		return latitude;
  	}
  	Location.getLongitude.implementation = function() {
      console.log(longitude);
      var longitude = parseFloat(longitude_inp)
  		return longitude;
  	}
  })
}

function bypassFlagSecure(){
   Java.perform(function() {
      // https://developer.android.com/reference/android/view/WindowManager.LayoutParams.html#FLAG_SECURE
      var FLAG_SECURE = 0x2000;

      var Runnable = Java.use("java.lang.Runnable");
      var DisableSecureRunnable = Java.registerClass({
         name: "me.bhamza.DisableSecureRunnable",
         implements: [Runnable],
         fields: {
            activity: "android.app.Activity",
         },
         methods: {
            $init: [{
               returnType: "void",
               argumentTypes: ["android.app.Activity"],
               implementation: function (activity) {
                  this.activity.value = activity;
               }
            }],
            run: function() {
               var flags = this.activity.value.getWindow().getAttributes().flags.value; // get current value
               flags &= ~FLAG_SECURE; // toggle it
               this.activity.value.getWindow().setFlags(flags, FLAG_SECURE); // disable it!
               console.log("Done disabling SECURE flag...");
            }
         }
      });

      Java.choose("com.example.maptmockapplication.MainActivity", {
       "onMatch": function (instance) {
            var runnable = DisableSecureRunnable.$new(instance);
            instance.runOnUiThread(runnable);
         },
         "onComplete": function () {}
      });
   });
}

rpc.exports = {
    enumerateactivities: enumerateActivities,
    gotoactivity: goToActivity,
    enumerateapplicationclasses: enumerateApplicationClasses,
    interceptsqlitequeries: interceptSQLiteQueries,
    printruntimestrings: printRunTimeStrings,
    changelocation: changeLocation,
    bypassflagsecure: bypassFlagSecure
};
