// construct the three series that render the different components of the MACD indicator
const divergenceBarSeries = fc.seriesSvgBar()
	.crossValue(d => d.date)
	.mainValue(d => d.macd.divergence);

const signalLineSeries = fc.seriesSvgLine()
	.crossValue(d => d.date)
	.mainValue(d => d.macd.signal)
  // use the decorator pattern to access the enter selection and add a class
  // to this series
	.decorate(sel =>
    sel.enter()
       .classed('signal', true)
  )

const macdLineSeries = fc.seriesSvgLine()
	.crossValue(d => d.date)
	.mainValue(d => d.macd.macd)
  .decorate(sel =>
    sel.enter()
       .classed('macd', true)
  );

// merge into a single seris which is associated with the chart
const mergedSeries_macd = fc.seriesSvgMulti()
	.series([divergenceBarSeries, signalLineSeries, macdLineSeries]);

// adapt the d3 time scale to add discontinuities, so that weekends are removed
const xScale_macd = fc.scaleDiscontinuous(d3.scaleTime())
  .discontinuityProvider(fc.discontinuitySkipWeekends());

const chart_macd = fc.chartSvgCartesian(
    xScale_macd,
    d3.scaleLinear()
  )
  .yOrient('left')
	.plotArea(mergedSeries_macd);

// use the extent component to determine the x domain
const xExtent_macd = fc.extentDate()
	.accessors([d => d.date]);

// the y domain should be symmetrical about the zero value and padded by 10%
const yExtent_macd = fc.extentLinear()
  .accessors([d => d.macd.macd])
	.pad([0.1, 0.1])
  .symmetricalAbout(0);

//const parseDate = d3.timeParse("%Y-%m-%d");

const macdAlgorithm = fc.indicatorMacd()
  .fastPeriod(12)
  .slowPeriod(26)
  .signalPeriod(9)
  .value(d => d.close);

function draw_chart_macd(file_name){
//    var url ='file_name + '?' + Math.floor(Math.random() * 1000');
    d3.csv(file_name + '?' + Math.floor(Math.random() * 1000) ,
      row => ({
        open: Number(row.Open),
        close: Number(row.Close),
        high: Number(row.High),
        low: Number(row.Low),
        date: parseDate(row.Date)
        })).then(data => {

        // the CSV data is in reverse date order
//        data = data.reverse();

        // compute the MACD
        const macdData = macdAlgorithm(data);

        // merge into a single series
        const mergedData = data.map((d, i) =>
          Object.assign({}, d, {
            macd: macdData[i]
          })
        );

        // set the domain based on the data
        chart_macd.xDomain(xExtent_macd(mergedData))
          .yDomain(yExtent_macd(mergedData));

        // select and render
        d3.select('#chart-element-macd')
          .datum(mergedData)
          .call(chart_macd);
      });
}
