require([
    'jquery',
    'splunkjs/mvc',
    'splunkjs/mvc/tableview',
    'splunkjs/mvc/simplexml/ready!'
], function($, mvc, TableView) {
    var venvs_search = mvc.Components.get('venvs_search');
    var RangeMapIconRenderer = TableView.BaseCellRenderer.extend({
        canRender: function(cell) {
            // Only use the cell renderer for the range field
            return cell.field === 'action';
        },
        render: function($td, cell) {
            // Create the icon element and add it to the table cell
            var verb;
            if (cell.value === "1") {
                $td.addClass('icon').html('<i class="icon-minus-circle red click"></i>');
                verb = "delete";
            } else {
                $td.addClass('icon').html('<i class="icon-plus-circle green click"></i>');
                verb = "create";
            }

            $td.on("click", function(){
                var search;
                var i = $(this.firstChild);
                i.addClass('icon-rotate');
                i.addClass('blue');
                i.addClass('spin');
                var tokens = mvc.Components.get("default");
                var env_version = tokens.get("env_version");
                var env_name = tokens.get("env_name");
                if (verb === "delete") {
                    i.removeClass("icon-minus-circle");
                    i.removeClass("red");
                    // ajax call to kick off createdist or pydelete, include callback to reload page
                    // determine create or delete
                    search = "| pydelete " + i.parent().parent().children()[1].innerHTML;
                } else if (verb === "create") {
                    i.removeClass("icon-plus-circle");
                    i.removeClass("green");
                    search = "| createvenv version=" + env_version + " name=" + env_name;
                }
                $.post(location.origin + "/en-US/splunkd/__raw/servicesNS/nobody/pyden-manager/search/jobs", {'exec_mode': 'oneshot', 'search': search}, function () {
                    // reload panel
                    venvs_search.startSearch();
                    location.href = location.origin + location.pathname
                })

            });
        }
    });
    mvc.Components.get('venvs_table').getVisualization(function(tableView){
        // Register custom cell renderer, the table will re-render automatically
        tableView.addCellRenderer(new RangeMapIconRenderer());
    });
    $('#submit > button').on("click", function (e) {
        // run search to set default to input token value and reload on succesfull callback
        var tokens = mvc.Components.get("default");
        var venv_default = tokens.get("venv_default");
        var job_url = location.origin + "/" + location.href.split("/")[3] + "/splunkd/__raw/servicesNS/nobody/pyden-manager/search/jobs";
        var params = {
            "exec_mode": "blocking",
            "search": "| changedefaultpys environment=" + venv_default
        };
        $.post(job_url, params, function() {window.location = window.location.href.split("?")[0];})
    });
});