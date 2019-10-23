$(document).ready(function () {

    //  chartist.js start

    /*
        ================================
                 statistics_data
        ================================
    */
    var alarm_data = document.getElementById('alarm_prt').getAttribute('chart_data');
    // var all_al=alarm_data.split("!")
    var mme_list = alarm_data.match(/MME\d+/g)
    var present_alarm = alarm_data.split(/HZMME\d+BNK/g)
    // var hist_alarm = all_al[1].split(/HZMME\d+BNK/g)
    // var normal = []
    // for (i = 0; i < presentation.length; i += 3) {
    //     normal.push(presentation[i])
    //     warning.push(presentation[i + 1])
    //     critical.push(presentation[i + 2])
    // }
    var chart = new Chartist.Bar('#statistics_data', {
            labels: mme_list,
            series: [
                //normal,
                // hist_alarm.slice(1,hist_alarm.length),
                present_alarm.slice(1, present_alarm.length)

            ]
        },
        {
            height: "190px",
            low: 0,
            showArea: true,
            showPoint: false,
            fullWidth: true,
            axisY: {
                labelInterpolationFnc: function (value) {
                    return value;
                }
            },
            plugins: [
                Chartist.plugins.tooltip({
                    currency: '重要告警数:',
                    class: 'line-graph-tooltip',
                    appendToBody: false,
                })
            ]
        });

    chart.on('draw', function (data) {
        if (data.type === 'line' || data.type === 'area') {
            data.element.animate({
                d: {
                    begin: 1000 * data.index,
                    dur: 2000,
                    from: data.path.clone().scale(1, 0).translate(0, data.chartRect.height()).stringify(),
                    to: data.path.clone().stringify(),
                    easing: Chartist.Svg.Easing.easeOutQuint
                }
            });
        }
    });


    /*
        ================================
                 product_status
        ================================
    */
    var data = {
        series: [35, 27, 23, 15]
    };

    var sum = function (a, b) {
        return a + b
    };

    new Chartist.Pie('#product_status', data, {
        labelInterpolationFnc: function (value) {
            return Math.round(value / data.series.reduce(sum) * 100) + '%';
        },
        height: "193px",
        plugins: [
            Chartist.plugins.tooltip({
                currency: '',
                class: 'line-graph-tooltip',
                appendToBody: false,
            })
        ]
    });

    /*
        ================================
                 yaerly_expence
        ================================
    */


    new Chartist.Bar('#yarly_expence', {
            labels: ['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            series: [
                [30000, 22000, 32000, 8000, 30000, 22000, 32000, 8000, 30000, 22000, 32000, 8000],
                [25000, 35000, 20000, 15000, 25000, 35000, 20000, 15000, 25000, 35000, 20000, 15000],
                [15000, 20000, 18000, 14000, 15000, 20000, 18000, 14000, 15000, 20000, 18000, 14000],
            ]
        },
        {
            height: "190px",
            // Default mobile configuration
            stackBars: true,
            axisX: {
                labelInterpolationFnc: function (value) {
                    return value.split(/\s+/).map(function (word) {
                        return word[0];
                    }).join('');
                }
            },
            axisY: {
                labelInterpolationFnc: function (value) {
                    return (value / 1000) + 'k';
                }
            },

            plugins: [
                Chartist.plugins.tooltip({
                    currency: '$',
                    class: 'line-graph-tooltip',
                    appendToBody: false,
                })
            ]
        },
        [
            // Options override for media > 400px
            ['screen and (min-width: 399px)', {}],
            // Options override for media > 800px
            ['screen and (min-width: 767px)', {
                stackBars: false,
                reverseData: true,
                horizontalBars: true,
                axisX: {
                    labelInterpolationFnc: Chartist.noop
                },
                axisY: {
                    offset: 60
                }

                // seriesBarDistance: 10
            }],
            // Options override for media > 1000px
            ['screen and (min-width: 768px)', {

                reverseData: false,
                horizontalBars: false,
                seriesBarDistance: 15
            }]
        ]
    );


    //  chartist.js end


});