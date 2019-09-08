 $(function () {
        //选择时分秒
        $('.J-datepicker-time').datePicker({
            format: 'HH:mm:ss',
            min: '04:23:11'
        });
        $('.J-datepicker-time-range').datePicker({
            format: 'HH:mm:ss',
            isRange: true,
            min: '04:23:11',
            max: '20:59:59'
        });
        //时分秒年月日单个
        $('.J-datepicker-en').datePicker({
            hasShortcut: true,
            min: '2018-01-01 04:00:00',
            max: '2019-04-29 20:59:59',
            language: 'en',
            shortcutOptions: [{
                name: 'today',
                day: '0'
            }, {
                name: 'yesterday',
                day: '-1',
                time: '00:00:00'
            }, {
                name: 'last week',
                day: '-7'
            }],
            hide: function () {
                console.info(this)
            }
        });
        var DATAPICKERAPI = {
            // 默认input显示当前月,自己获取后填充
            activeMonthRange: function () {
                return {
                    begin: moment().set({'date': 1, 'hour': 0, 'minute': 0, 'second': 0}).format('YYYY-MM-DD HH:mm:ss'),
                    end: moment().set({'hour': 23, 'minute': 59, 'second': 59}).format('YYYY-MM-DD HH:mm:ss')
                }
            },
            shortcutMonth: function () {
                // 当月
                var nowDay = moment().get('date');
                var prevMonthFirstDay = moment().subtract(1, 'months').set({'date': 1});
                var prevMonthDay = moment().diff(prevMonthFirstDay, 'days');
                return {
                    now: '-' + nowDay + ',0',
                    prev: '-' + prevMonthDay + ',-' + nowDay
                }
            },
            // 近n小时计算返回
            shortcutPrevHours: function (hour) {
                var nowDay = moment().get('date');
                var prevHours = moment().subtract(hour, 'hours');
                var prevDate = prevHours.get('date') - nowDay;
                var nowTime = moment().format('HH:mm:ss');
                var prevTime = prevHours.format('HH:mm:ss');
                return {
                    day: prevDate + ',0',
                    time: prevTime + ',' + nowTime,
                    name: '近' + hour + '小时'
                }
            },
            // 注意为函数：快捷选项option:只能同一个月份内的
            rangeMonthShortcutOption1: function () {
                var result = DATAPICKERAPI.shortcutMonth();
                // 近18小时
                var resultTime = DATAPICKERAPI.shortcutPrevHours(18);
                return [{
                    name: '昨天',
                    day: '-1,-1',
                    time: '00:00:00,23:59:59'
                }, {
                    name: '这一月',
                    day: result.now,
                    time: '00:00:00,'
                }, {
                    name: '上一月',
                    day: result.prev,
                    time: '00:00:00,23:59:59'
                }, {
                    name: resultTime.name,
                    day: resultTime.day,
                    time: resultTime.time
                }];
            },
            // 快捷选项option
            rangeShortcutOption1: [{
                name: '最近一周',
                day: '-7,0'
            }, {
                name: '最近一个月',
                day: '-30,0'
            }, {
                name: '最近三个月',
                day: '-90, 0'
            }],
            singleShortcutOptions1: [{
                name: '今天',
                day: '0',
                time: '00:00:00'
            }, {
                name: '昨天',
                day: '-1',
                time: '00:00:00'
            }, {
                name: '一周前',
                day: '-7'
            }]
        };
        //时分秒年月日单个
        $('.J-datepicker').datePicker({
            hasShortcut: true,
            min: '2018-01-01 04:00:00',
            max: '2019-04-29 20:59:59',
            shortcutOptions: [{
                name: '今天',
                day: '0'
            }, {
                name: '昨天',
                day: '-1',
                time: '00:00:00'
            }, {
                name: '一周前',
                day: '-7'
            }],
            hide: function () {
                console.info(this)
            }
        });

        //年月日单个
        $('.J-datepicker-day').datePicker({
            hasShortcut: true,
            format: 'YYYY-MM-DD',
            shortcutOptions: [{
                name: '今天',
                day: '0'
            }, {
                name: '昨天',
                day: '-1'
            }, {
                name: '一周前',
                day: '-7'
            }]
        });

        //年月日范围
        $('.J-datepicker-range-day').datePicker({
            hasShortcut: true,
            format: 'YYYY-MM-DD',
            isRange: true,
            shortcutOptions: DATAPICKERAPI.rangeShortcutOption1
        });

        //十分年月日单个
        $('.J-datepickerTime-single').datePicker({
            format: 'YYYY-MM-DD HH:mm'
        });

        //十分年月日范围
        $('.J-datepickerTime-range').datePicker({
            format: 'YYYY-MM-DD HH:mm',
            isRange: true
        });

        //时分秒年月日范围，包含最大最小值
        $('.J-datepicker-range').datePicker({
            hasShortcut: true,
            min: '2018-01-01 06:00:00',
            max: '2019-04-29 20:59:59',
            isRange: true,
            shortcutOptions: [{
                name: '昨天',
                day: '-1,-1',
                time: '00:00:00,23:59:59'
            }, {
                name: '最近一周',
                day: '-7,0',
                time: '00:00:00,'
            }, {
                name: '最近一个月',
                day: '-30,0',
                time: '00:00:00,'
            }, {
                name: '最近三个月',
                day: '-90, 0',
                time: '00:00:00,'
            }],
            hide: function (type) {
                console.info(this.$input.eq(0).val(), this.$input.eq(1).val());
                console.info('类型：', type)
            }
        });
        //时分秒年月日范围，限制只能选择同一月，比如2018-10-01到2018-10-30
        $('.J-datepicker-range-betweenMonth').datePicker({
            isRange: true,
            between: 'month',
            hasShortcut: true,
            shortcutOptions: DATAPICKERAPI.rangeMonthShortcutOption1()
        });

        //时分秒年月日范围，限制开始结束相隔天数小于30天
        $('.J-datepicker-range-between30').datePicker({
            isRange: true,
            between: 30
        });

        //年月单个
        $('.J-yearMonthPicker-single').datePicker({
            format: 'YYYY-MM',
            min: '2018-01',
            max: '2019-04',
            hide: function (type) {
                console.info(this.$input.eq(0).val());
            }
        });

        //选择年
        $('.J-yearPicker-single').datePicker({
            format: 'YYYY',
            min: '2018',
            max: '2020'
        });

        // $('#starttime').datepicker({ onClose: function(dateText, inst) { alert("666") } });
        //         $('#endtime').datepicker({ onClose: function(dateText, inst) { alert("999") } });
    });