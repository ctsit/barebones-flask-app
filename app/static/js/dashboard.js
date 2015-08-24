// Implements the UI for...
//
//  Components used:
//
//      Dashboard

var Dashboard = React.createClass({
        getInitialState: function() {
        //Add Listner for the url change
        window.onhashchange = this.urlChanged;

        var tabs = [
            "Tab 1",
            "Tab 2",
            "Tab 3"
        ];
        return {
            current_tab: 0,
            tabs: tabs,
        };
    },
    changeTab: function(i) {
        this.setState({
            current_tab: i
        });
    },
    dataSelected: function(data) {
        this.setState({
            current_tab: 1,
            data: data
        });
    },

    render: function() {
        return (
            <div> ReactJS </div>
        );
    }
});

React.render(<Dashboard/>, document.getElementById("dashboard"));
