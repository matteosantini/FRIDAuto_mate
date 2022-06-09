// Returns the list [id] -> activity_name
function enumerateActivities(package_name){
  Java.perform(function(){
  var rclass = Java.use(`${package_name}.R$layout]`);//
  var arr = Object.keys(rclass);
  console.log("*********************************");
  console.log("ENUMERATING ACTIVITIES");
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

//takes the activity index from python, it hooks the onStart executing setContentView()
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

rpc.exports = {
    enumerateactivities: enumerateActivities,
    gotoactivity: goToActivity
};
