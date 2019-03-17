 function getRandomColor() {
        var letters = '0123456789ABCDEF'.split('');
        var color = '#';
        for (var i = 0; i < 6; i++ ) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }

const SMILEY = {
	'happy': happy,
	'sad': sad,
	'neutral': neutral
}
console.log(sentiment_data);

all_data = []
for (var i = 0; i < sentiment_data.length; i++) {
	var color = getRandomColor()
	all_data.push({
		label: sentiment_data[i].key,
		borderColor: color,
		backgroundColor: color,
		showLine: true,
		fill: false,
		data: [],
		pointStyle: []
	});

	for (var j = 0; j < sentiment_data[i].data.length; j++) {
		all_data[i].data.push({x: sentiment_data[i].data[j][0], y: sentiment_data[i].data[j][1]});
		
		emotion = sentiment_data[i].data[j][1] > 0.2 ? 'happy' : (sentiment_data[i].data[j][1] < -0.2 ? 'sad' : 'neutral');

		var img = new Image()
		img.src = SMILEY[emotion];
		img.height = 20;
		img.width = 20;
		
		all_data[i].pointStyle.push(img);
	}
}
var color = Chart.helpers.color;
		var scatterChartData = {
			datasets: all_data
		};

		window.onload = function() {
			var ctx = document.getElementById('sentiment-chart').getContext('2d');
			ctx.height = 400;
			window.myScatter = Chart.Scatter(ctx, {
				data: scatterChartData,
				options: {
					responsive: true,
	  				maintainAspectRatio: false,
					title: {
						display: true,
						text: 'Group Sentiment Graph'
					},
					scales: {
			            xAxes: [{
			                // This is the important part
			                type: "time",
			                time: {
			                	unit: 'day'
			                }
			            }],
			            yAxes: [{
					        ticks: {
					          beginAtZero: false,
					          min: -1,
					          max: 1,
					          stepSize: 0.2,
					        }
					      }]
			        },
			        tooltips: {
				      callbacks: {
				      	title: function(tooltipItems, data) {
				          return '';
				        },
				        label: function(tooltipItem, data) {
				          var datasetLabel = '';
				          var label = data.labels[tooltipItem.index];
				          return parseFloat(data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index].y).toFixed(2);
				        }
				      }
				    }
				}
			});
		};