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
function enumerateLoadedClasses(class_name = null){
  Java.perform(function() {
      Java.enumerateLoadedClasses({
          onMatch: function(className) {
              // if(className.includes("MainActivity")){
                console.log(`[CLASS] ${className}.R$layout`);
              // }
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

rpc.exports = {
    enumerateactivities: enumerateActivities,
    gotoactivity: goToActivity,
    enumerateloadedclasses: enumerateLoadedClasses,
    interceptsqlitequeries: interceptSQLiteQueries,
};
