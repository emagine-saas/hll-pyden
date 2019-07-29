require.config({
    paths: {
        "marked": "../../app/pyden-manager/marked.min"
    }
});

require([
    'underscore',
    'jquery',
    'marked',
    'splunkjs/mvc',
    'splunkjs/mvc/tableview',
    'splunkjs/mvc/simplexml/ready!'
], function (_, $, marked, mvc, TableView) {
    var RangeMapIconRenderer = TableView.BaseCellRenderer.extend({
        canRender: function (cell) {
            // Only use the cell renderer for the range field
            return cell.field === 'package';
        },
        render: function ($td, cell) {
            var tokenset = mvc.Components.get("default");
            var pypiPackage = cell.value;
            var search = `| getpackages ${pypiPackage}`;
            var searchUrl = location.origin + "/en-US/splunkd/__raw/servicesNS/nobody/pyden-manager/search/jobs";
            $td.html(pypiPackage);
            var submitButton = '<div id="submit" class="splunk-submit-button form-submit dashboard-form-submit"><button class="btn btn-primary">Install</button></div>';
            var rotate_icon = '<div id="rotate_icon" class="splunk-submit-button form-submit dashboard-form-submit icon"><i class="icon-rotate blue spin"></i></div>';
            var done_icon = '<div id="done_icon" class="splunk-submit-button form-submit dashboard-form-submit icon"><i class="icon-check-circle green"></i></div>';
            var error_icon = '<div id="done_icon" class="splunk-submit-button form-submit dashboard-form-submit icon"><i class="icon-minus-circle red"></i></div>';
            $td.on("click", function (e) {
                $.post(location.origin + "/en-US/splunkd/__raw/servicesNS/nobody/pyden-manager/search/jobs", {
                    'exec_mode': 'oneshot',
                    'search': search,
                    'output_mode': 'json'
                }, function (data) {
                    var desc = mvc.Components.get('description');
                    var venv = $('#venv');
                    venv.nextAll('div').remove();
                    venv.after(submitButton);
                    var md = data.results[0].description;
                    var tokens = marked.lexer(md);
                    desc.el.innerHTML = marked.parser(tokens);

                    tokenset.on("change:environment", function () {
                        var environment = tokenset.get("environment");
                        var submit = $('#submit');
                        $.post(searchUrl, {
                            'exec_mode': 'oneshot',
                            'output_mode': 'json',
                            'search': `| pip environment=${environment} freeze | eval package=mvindex(split(messages, "=="), 0) | search package=${pypiPackage}`
                        }, function (data) {
                            console.log(data.results.length);
                            if (data.results.length > 0) {
                                submit.find('button').prop('disabled', true);
                                submit.on("click", function (e) {
                                    $('#done_icon').remove();
                                    submit.after(rotate_icon);
                                    $.post(searchUrl, {
                                        'exec_mode': 'oneshot',
                                        'output_mode': 'json',
                                        'search': `| pip environment=${environment} install ${pypiPackage}`
                                    }, function (data) {
                                        $('#rotate_icon').remove();
                                        if (data.messages.length > 0 && data.messages[0].type === "ERROR") {
                                            submit.after(error_icon);
                                        } else {
                                            submit.after(done_icon);
                                        }
                                    }).fail(function(){
                                        $('#rotate_icon').remove();
                                        submit.after(error_icon);
                                    })
                                })
                            } else {
                                submit.find('button').prop('disabled', false);
                            }
                        });

                    });

                })
            });
        }
    });
    mvc.Components.get('package_table').getVisualization(function (tableView) {
        // Register custom cell renderer, the table will re-render automatically
        tableView.addCellRenderer(new RangeMapIconRenderer());
    });
});