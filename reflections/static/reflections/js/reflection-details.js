$(document).ready(function(){

	function sortProperties(obj)
	{
	  // convert object into array
		var sortable=[];
		for(var key in obj)
			if(obj.hasOwnProperty(key))
				sortable.push([key, obj[key]]); // each item is an array in format [key, value]
		
		// sort items by value
		sortable.sort(function(a, b)
		{
			var x=a[1],
				y=b[1];
			return x>y ? -1 : x<y ? 1 : 0;
		});
		return sortable; // array in format [ [ key1, val1 ], [ key2, val2 ], ... ]
	}

	// Set new default font family and font color to mimic Bootstrap's default styling
	Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
	Chart.defaults.global.defaultFontColor = '#292b2c';

	
	var sortedlist = sortProperties(wordList);
	sortedlist.length = sortedlist.length > 15 ? 15 : sortedlist.length;

	var wordLabel = [];
	var wordCount = [];
	for(var key in sortedlist){
		wordLabel.push(sortedlist[key][0]);
		wordCount.push(sortedlist[key][1]);
	}
	
	var maxValue = Math.max.apply(null,wordCount);

	// Bar Chart Example
	var ctx = document.getElementById("myBarChart");
	var myLineChart = new Chart(ctx, {
	  height: 250,
	  type: 'bar',
	  data: {
	    labels: wordLabel,
	    datasets: [{
	      label: "Word Count",
	      backgroundColor: "rgba(2,117,216,1)",
	      borderColor: "rgba(2,117,216,1)",
	      data: wordCount,
	    }],
	  },
	  options: {
	  	responsive: true,
	  	maintainAspectRatio: false,
	    scales: {
	      xAxes: [{
	        time: {
	          unit: 'words'
	        },
	        gridLines: {
	          display: false
	        },
	        ticks: {
	          maxTicksLimit: 15
	        }
	      }],
	      yAxes: [{
	        ticks: {
	          min: 0,
	          max: maxValue,
	          maxTicksLimit: maxValue/2
	        },
	        gridLines: {
	          display: true
	        }
	      }],
	    },
	    legend: {
	      display: false
	    }
	  }
	});

});