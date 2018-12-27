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
                    var submit = $('#submit');
                    submit.on("click", function (e) {
                        submit.after(rotate_icon);
                        var environment = tokenset.get("environment");
                        $.post(location.origin + "/en-US/splunkd/__raw/servicesNS/nobody/pyden-manager/search/jobs", {
                            'exec_mode': 'oneshot',
                            'output_mode': 'json',
                            'search': `| pip environment=${environment} install ${pypiPackage}`
                        }, function (data) {
                            $('#rotate_icon').remove();
                            console.log(data);
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
                })
            });
        }
    });
    mvc.Components.get('package_table').getVisualization(function (tableView) {
        // Register custom cell renderer, the table will re-render automatically
        tableView.addCellRenderer(new RangeMapIconRenderer());
    });
});