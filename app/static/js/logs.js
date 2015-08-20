// Implement two components
//  AdminEventsTable - ...
//  AdminEventsPagination - ...

var AdminEventsTable = React.createClass({
    getInitialState: function() {
        return {
            list_of_events: this.props.list_of_events
        };
    },
    componentWillReceiveProps: function(nextProps) {
        this.setState({
            list_of_events: nextProps.list_of_events
        });
    },
    render: function() {
        return (
        <div className="table-responsive">
            <table className="table borderless sortable">
                <thead>
                    <tr>
                        <th className="text-right"> ID </th>
                        <th className="text-left"> User Email </th>
                        <th className="text-left"> Type </th>
                        <th className="text-left" width="40%"> Details </th>
                        <th className="text-left"> WebSession IP </th>
                        <th className="text-right"> Date</th>
                    </tr>
                </thead>
                <tbody>
                {
                    this.state.list_of_events.map(function(record, i) {
                        return (<tr>
                                <td className="text-right"> {record.id}</td>
                                <td className="text-left"> {record.user_email} </td>
                                <td className="text-left"> {record.type}</td>
                                <td className="text-left"> {record.details}</td>
                                <td className="text-left"> {record.web_session_ip}</td>
                                <td className="text-right"> {record.date_time}</td>
                                </tr>
                               );
                    })
                }
                </tbody>
            </table>
        </div>
        );
    }
});

var AdminEventsPagination = React.createClass({
    getInitialState: function() {
        return {
            total_pages: this.props.total_pages,
            current_page: 1
        };
    },
    componentWillReceiveProps: function(nextProps) {

    },
    activateOnClick: function(i) {
        this.setState({
            total_pages: this.state.total_pages,
            current_page: i
        });
        this.props.changePage(i);
    },
    nextPage: function() {
        var current_page = this.state.current_page;

        if(current_page === this.state.total_pages) {
            return;
        }

        this.setState({
            total_pages: this.state.total_pages,
            current_page: current_page+1
        });
        this.props.changePage(current_page+1);
    },
    prevPage: function() {
        var current_page = this.state.current_page;

        if(current_page === 1) {
            return;
        }
        this.setState({
            total_pages: this.state.total_pages,
            current_page: current_page-1
        });
        this.props.changePage(current_page-1);
    },
    render: function() {
        var pages = [];

        for(var i = 1; i <= this.state.total_pages; i++) {
            if (i === this.state.current_page) {
                pages.push(<li className="active"><a>{i}</a></li>);
            }
            else {
                pages.push(<li><a onClick={this.activateOnClick.bind(null, i)}> {i} </a></li>);
            }
        }
        return (
                <nav>
                <ul className="pagination">
                <li>
                <a onClick={this.prevPage} aria-label="Previous">
                <span aria-hidden="true">&laquo;</span>
                </a>
                </li>
                {pages}
                <li>
                <a onClick={this.nextPage} aria-label="Next">
                <span aria-hidden="true">&raquo;</span>
                </a>
                </li>
                </ul>
                </nav>
               );
    }
});

var AdminEventsList = React.createClass({
    getInitialState: function() {
        return {
            list_of_events: undefined,
            total_pages: 0,
            per_page: 25
        };
    },
    componentWillMount: function() {
        var _this = this;
        var request_data = {'per_page': this.state.per_page, 'page_num': '1'};
        var request = Utils.api_post_json("/api/list_logs", request_data);

        request.success( function(json) {
            _this.setState({
                list_of_events: json.data.list_of_events,
                total_pages: json.data.total_pages
            });
            $(".sortable").tablesorter();
        });
        request.fail(function (jqXHR, textStatus, error) {
            console.log('Failed: ' + textStatus + error);
        });
    },
    changePage: function(page_num) {
        var _this = this;
        var request_data = {'per_page': this.state.per_page, 'page_num': page_num};
        var request = Utils.api_post_json("/api/list_logs", request_data);

        request.success(function(json) {
            _this.setState({
                list_of_events: json.data.list_of_events,
                total_pages: json.data.total_pages
            });
        });
        request.fail(function (jqXHR, textStatus, error) {
            console.log('Failed: ' + textStatus + error);
        });
    },
    render: function() {
        var total_pages = this.state.total_pages;
        var list_of_events = this.state.list_of_events;
        var pagination;

        if(total_pages > 1) {
            pagination = <AdminEventsPagination total_pages={total_pages} changePage={this.changePage}/>;
        }
        var events_table;
        if(list_of_events === undefined) {
            //@TODO: show a "loading" animation
        }
        else if(list_of_events.length === 0) {
             events_table = <div>There is no data to display. If you think this is an error please contact your support personnel.</div>;
        }
        else {
            events_table = <AdminEventsTable list_of_events = {this.state.list_of_events}/>;
        }
        return (
                <div>
                {events_table}
                {pagination}
                </div>
               );
    }
});

React.render(<AdminEventsList/>, document.getElementById("admin-events-list"));
