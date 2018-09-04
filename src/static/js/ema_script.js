//const parseDate = d3.timeParse("%Y-%m-%d");

function draw_EMA(file_name){
    d3.csv(file_name,
        row => ({
          	open: Number(row.Open),
          	close: Number(row.Close),
          	high: Number(row.High),
          	low: Number(row.Low),
          	date: parseDate(row.Date)
        	})).then(data =>{

          // compute a 20 point ema
          var ema20 = fc.exponentialMovingAverage()
              .value(function(d) { return d.close; })
              // the merge function describes how the ema is 'stored' in each datapoint
              .merge(function(datum, ema) { datum.ema20 = ema; })
              .windowSize(20);

          // compute a 40 point ema
          var ema40 = fc.indicator.algorithm.exponentialMovingAverage()
              .value(function(d) { return d.close; })
              .merge(function(datum, ema) { datum.ema40 = ema; })
              .windowSize(40);

          // compute the algorithms
          ema20(data);
          ema40(data);

          var chart = fc.chart.linearTimeSeries()
                .xDomain(fc.util.extent(data, 'date'))
                .yDomain(fc.util.extent(data, ['open', 'close']));

          var area = fc.series.area()
                .yValue(function(d) { return d.open; });

          var ema20Line = fc.series.line()
                .yValue(function(d) { return d.ema20; })
                .decorate(function(sel) {
                  sel.classed('ema20', true);
                });

          var ema40Line = fc.series.line()
                .yValue(function(d) { return d.ema40; })
                .decorate(function(sel) {
                  sel.classed('ema40', true);
                });


          var multi = fc.series.multi()
                .series([area, ema20Line, ema40Line]);

          chart.plotArea(multi);

          d3.select('#time-series')
                .datum(data)
                .call(chart);
        })
}
