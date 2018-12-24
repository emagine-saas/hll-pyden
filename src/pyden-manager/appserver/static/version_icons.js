require([
    'underscore',
    'jquery',
    'splunkjs/mvc',
    'splunkjs/mvc/tableview',
    'splunkjs/mvc/simplexml/ready!'
], function(_, $, mvc, TableView) {
    var ICONS = {
        0: 'plus-circle',
        1: 'minus-circle'
    };
    var RANGE = {
        0: 'green',
        1: 'red'
    };
    var invICONS = {
        'plus-circle': 0,
        'minus-circle': 1
    };
    var RangeMapIconRenderer = TableView.BaseCellRenderer.extend({
        canRender: function(cell) {
            // Only use the cell renderer for the range field
            return cell.field === 'status';
        },
        render: function($td, cell) {
            var icon = "plus-circle";
            var range = "green";

            // Fetch the icon for the value
            if (ICONS.hasOwnProperty(cell.value)) {
                icon = ICONS[cell.value];
                range = RANGE[cell.value];
            }
            // Create the icon element and add it to the table cell
            $td.addClass('icon').html(_.template('<i class="icon-<%-icon%> <%- range %>"></i>', {
                icon: icon,
                range: range
            }));
            $td.on("click", function(e){
                var i = $(this.firstChild);
                i.removeClass("icon-" + icon);
                i.removeClass(range);
                i.addClass(icon);
                i.addClass('icon-rotate');
                i.addClass('blue');
                i.addClass('spin');
                // ajax call to kick off createdist or pydelete, include callback to reload page
                // determine create or delete
                var search;
                if (range === "green") {
                    search = "| createdist version=" + i.parent().parent().children()[1].innerHTML;
                } else if (range === "red") {
                    search = "| pydelete " + i.parent().parent().children()[1].innerHTML;
                }
                $.post(location.origin + "/en-US/splunkd/__raw/servicesNS/nobody/pyden-manager/search/jobs", {'exec_mode': 'oneshot', 'search': search}, function () {
                    i.removeClass('icon-rotate');
                    i.removeClass('blue');
                    i.removeClass('spin');
                    var oldValue = invICONS[icon];
                    var newValue = (oldValue + 1) % 2;
                    icon = ICONS[newValue];
                    range = RANGE[newValue];
                    i.addClass('icon-' + icon);
                    i.addClass(range);
                })
            });
        }
    });
    mvc.Components.get('version_table').getVisualization(function(tableView){
        // Register custom cell renderer, the table will re-render automatically
        tableView.addCellRenderer(new RangeMapIconRenderer());
    });
});