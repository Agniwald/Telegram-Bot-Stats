var active = '';

function show(labels_to_show, datasets_to_show, lang_data){
	var ctx = document.getElementById('myChart').getContext('2d');

  var parsed_datasets = [];
  for (var i = 0; i < datasets_to_show.length; i++) {
    parsed_datasets.push({
      label: datasets_to_show[i]['label'],
      backgroundColor: datasets_to_show[i]['backgroundColor'],
      borderColor: datasets_to_show[i]['borderColor'],
      data: datasets_to_show[i]['data'],
      fill: false,
      trendlineLinear: {
        style: datasets_to_show[i]['backgroundColor'],
        lineStyle: "dotted",
        width: 2
      }
    });
  }

  var chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: labels_to_show,
        datasets: parsed_datasets
    },
    options: {}
  });

  var ctx2 = document.getElementById('myChart2').getContext('2d');
  var chart2 = new Chart(ctx2, {
    type: 'doughnut',
    data: lang_data,
    options: {}
  });
}


function change_range(range){
  var li = document.getElementById(range);
  if (!li.classList.contains("active")){
    var otherli = document.getElementsByTagName("li");

    for (let i = 0; i < otherli.length; i++)
      otherli[i].classList.remove("active")
    
    li.classList.add("active");
  }
}

function fetch(bot, range){
  if (bot == ''){
    bot = active;
  }

  document.getElementById("name").innerHTML = "Fetching and processing data...";
	var xhttp = new XMLHttpRequest();
  xhttp.responseType = 'json';
  xhttp.open('GET', "/" + bot + "/" + range, true);
  xhttp.onload  = function() {
    var jsonResponse = xhttp.response;
    show(jsonResponse['labels'], jsonResponse['datasets'], jsonResponse['lang_data']);
    document.getElementById("name").innerHTML = bot;
  };
	xhttp.send();

  change_range(range);
  active = bot;
}