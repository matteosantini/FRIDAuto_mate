//DEBUG PAGE
//frida -U -l activityswap.js -f com.example.maptmockapplication --no-pause
Java.perform(function () {
    //from activity
    var mainactivity = Java.use('com.example.maptmockapplication.MainActivity');
    //to activity
    var swapactivity = Java.use('com.example.maptmockapplication.SwapActivity');
    var appCompatActivity = Java.use('androidx.appcompat.app.AppCompatActivity');
    var rclass = Java.use("com.example.maptmockapplication.R$layout");
    var main = rclass.activity_main.value
    var not_link = rclass.activity_not_linkable.value;
    var swap = rclass.activity_swap.value;

    console.log(swap);
    console.log(rclass);

});

Interceptor.attach(Module.findExportByName('libsqlite.so', 'sqlite3_prepare16_v2'), {
      onEnter: function(args) {
          console.log('DB: ' + Memory.readUtf16String(args[0]) + '\tSQL: ' + Memory.readUtf16String(args[1]));
      }
});
    // console.log("====");
    // Java.perform(function() {
    //     Java.enumerateLoadedClasses({
    //         onMatch: function(className) {
    //             if(className.includes("MainActivity")){
    //               console.log(className);
    //             }
    //         },
    //         onComplete: function() {}
    //     });
    // });
    //com.example.maptmockapplication.MainActivity
    //com.example.maptmockapplication.MainActivity$$ExternalSyntheticLambda0

    // mainactivity.onStart.overload().implementation = function () {
    //   send('onResume() got called! Let\'s call the original implementation');
    //   var rclass = Java.use("com.example.maptmockapplication.R$layout");
    //   var main = rclass.activity_not_linkable.value
    //   var a = appCompatActivity.$new();
    //   a.setContentView(not_link);
    //   var ret = this.onStart().overload().call(this);
    // };

   //  Java.scheduleOnMainThread(function () {
   //     send(Java.isMainThread());
   //     var a = mainactivity.$new();
   //     a.setContentView(not_link);
   // });

  //  Java.scheduleOnMainThread(function () {
  //     send(Java.isMainThread());
  //     var a = appCompatActivity.$new();
  //     a.setContentView(2131427356);
  // });



    // function changeActivity(){
    //   var looper=Java.use("android.os.Looper");
    //   looper.prepare();
      // var rclass = Java.use("com.example.maptmockapplication.R$layout");
      // var main = rclass.activity_not_linkable.value;
      // console.log(main);
      // var a = appCompatActivity.$new();
      // a.setContentView(main);
    // }

    // mainactivity.onCreate.overload("android.os.Bundle").implementation = function (var_0) {
    //   send('onCreate() got called! Let\'s call the original implementation');
    //   console.log(var_0);
    //   var ret = this.onCreate.overload("android.os.Bundle").call(this,var_0);
    // };
    // mainactivity.onResume.implementation = function () {
    //   send('onResume() got called! Let\'s call the original implementation');
    //   var rclass = Java.use("com.example.maptmockapplication.R$layout");
    //   var main = rclass.activity_not_linkable.value
    //   console.log(main);
    //   var a = appCompatActivity.$new();
    //   a.setContentView(main);
    //   var ret = this.onResume();
    // };


    // UTILE
    // Java.enumerateLoadedClasses({
    //     onMatch: function(className) {
    //         if (className.includes("com.example.maptmockapplication")) {
    //             console.log(className);
    //         }
    //     },
    //     onComplete: function() {}
    // });

    //UTILE
    // function describeJavaClass(className) {
    //   var jClass = Java.use(className);
    //   console.log(JSON.stringify({
    //     _name: className,
    //     _methods: Object.getOwnPropertyNames(jClass.__proto__).filter(m => {
    //       return !m.startsWith('$') // filter out Frida related special properties
    //          || m == 'class' || m == 'constructor' // optional
    //     }),
    //     _fields: jClass.class.getFields().map(f => {
    //       return f.toString()
    //     })
    //   }, null, 2));
    // }
