// create two different series types for rendering the data
const candlestickSeries = fc.seriesSvgCandlestick()
	.bandwidth(3);

const movingAverageSeries = fc.seriesSvgLine()
  .mainValue(d => d.ma)
  .crossValue(d => d.date)
  .decorate(sel =>
      sel.enter()
          .classed('ma', true)
    );

const movingAverageSeries12 = fc.seriesSvgLine()
  .mainValue(d => d.ma12)
  .crossValue(d => d.date)
  .decorate(sel =>
    sel.enter()
        .classed('ma12', true)
    );

const movingAverageSeries26 = fc.seriesSvgLine()
  .mainValue(d => d.ma26)
  .crossValue(d => d.date)
  .decorate(sel =>
    sel.enter()
        .classed('ma26', true)
  );

// RSI
const rsi = fc.seriesSvgLine()
    .crossValue(function(d) { return d.date; })
    .mainValue(function(d) { return d.rsi; });

// merge into a single series that is associated with the chart
const mergedSeries = fc.seriesSvgMulti()
	.series([movingAverageSeries, candlestickSeries]);

// adapt the d3 time scale to add discontinuities, so that weekends are removed
const xScale = fc.scaleDiscontinuous(d3.scaleTime())
  .discontinuityProvider(fc.discontinuitySkipWeekends());

const chart = fc.chartSvgCartesian(
    xScale,
    d3.scaleLinear()
  )
	.yOrient('left')
	.plotArea(mergedSeries);

// use the extent component to determine the x and y domain
const durationDay = 864e5;
const xExtent = fc.extentDate()
	.accessors([d => d.date])
	// pad by one day on either side of the scale
	.padUnit('domain')
	.pad([durationDay, durationDay]);

// the y extent is based on the high / lowr values, which provide the two extremes
const yExtent = fc.extentLinear()
	.accessors([d => d.high, d => d.low])
	// pad by 10% up and down
	.pad([0.1, 0.1]);

//const parseDate = d3.timeParse("%d-%b-%y");
const parseDate = d3.timeParse("%Y-%m-%d");

const ma = fc.indicatorMovingAverage().period(12)
    .value(d => d.open);

const ma12 = fc.indicatorMovingAverage().period(12)
    .value(d => d.open);

const ma26 = fc.indicatorMovingAverage().period(26)
    .value(d => d.open);

function draw_chart(file_name) {
    //d3.csv('../static/data/data.csv',
//    '../static/data/aapl.csv',
    d3.csv(file_name,
      row => ({
        open: Number(row.Open),
        close: Number(row.Close),
        high: Number(row.High),
        low: Number(row.Low),
        date: parseDate(row.Date)
        })).then(data => {

        data = data.reverse();

        // compute the moving average data
        const maData = ma(data);
        const maData12 = ma12(data);
        const maData26 = ma26(data);

        // merge into a single series
        const mergedData = data.map((d, i) =>
          Object.assign({}, d, {
            ma: maData[i]
//            ,
//            ma12: maData12[i],
//            ma26: maData26[i]
          })
        );

        // set the domain based on the data
        chart.xDomain(xExtent(mergedData))
          .yDomain(yExtent(mergedData))

        // select and render
        d3.select('#chart-element')
          .datum(mergedData)
          .call(chart);
      });
}