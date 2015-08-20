// Implements the UI for displaying subject event files
//
//  Components used:
//
//      SubjectsRow
//      SubjectsTable
//      SubjectsPagination
//
//      EventsTable
//      FilesList
//      Dashboard

var SubjectsRow = React.createClass({
    getInitialState: function() {
        return {
            row_data: this.props.row_data,
            max_events: this.props.max_events
        };
    },
    componentWillReceiveProps: function(nextProps) {
        this.setState({
            row_data: nextProps.row_data,
            max_events: nextProps.max_events
        });
    },
    /*
    showAlert: function() {
        $("#event-alert").show();
        setTimeout(function () {
            $("#event-alert").hide();
        }, 1500);
    },
    */
    render: function() {
        var column_count = this.state.max_events;
        var table_columns = [];
        var row_data = this.state.row_data;
        var events_count = 0;
        var i;

        /*
        for (i = events_count + 2; i <= column_count; i++) {
            table_columns.push(<td><i className="fa fa-lg fa-plus-circle" onClick={this.showAlert}></i></td>);
        }
        */

        var selectSubject = this.props.subjectSelected.bind(null, row_data);
        return (
            <tr>
                <td>
                    <button className="btn btn-lg2 btn-primary"
                        onClick={selectSubject}>
                        Select subject: {row_data.redcap_id}
                    </button>
                </td>
                {table_columns}
            </tr>
       );
    }
});


var SubjectsTable = React.createClass({

    getInitialState: function() {
        return {
            subjects: [],
            max_events: this.props.max_events,
            no_of_pages: 0
        };
    },
    changePage: function(i) {
        this.changeData(i, this.state.max_events);
    },
    changeData: function(page_num, max_events) {
        // if needed we will allow the user to select how many rows to display per page
        var per_page = 25;
        var request_data = {'per_page': per_page, 'page_num': page_num};
        var _this = this;
        var request = Utils.api_post_json("/api/list_local_subjects", request_data);

        request.success( function(json) {
            _this.setState({
                subjects: json.data.list_of_subjects,
                max_events: max_events,
                no_of_pages: json.data.total_pages
            });
        });
        request.fail(function (jqXHR, textStatus, error) {
            console.log('Failed: ' + textStatus + error);
        });
    },
    componentWillMount: function() {
        this.changeData(1, this.props.max_events);
    },
    componentWillReceiveProps: function(nextProps) {
        this.changeData(1, nextProps.max_events);
    },
    render: function() {
        var table_rows = [];
        var subjects_data = this.state.subjects;
        var row_count = subjects_data.length;
        var column_count = this.state.max_events;

        var i;
        for(i = 0; i < row_count; i++) {
            table_rows.push(<SubjectsRow
                    row_data = {subjects_data[i]}
                    max_events = {column_count}
                    subjectSelected = {this.props.subjectSelected}/>);
        }

        var table_columns = [];
        for (i = 1; i <= column_count; i++) {
            table_columns.push(<th> Event {i}</th>);
        }

        var pagination;
        var no_of_pages = this.state.no_of_pages;

        if (no_of_pages > 1) {
            pagination = <SubjectsPagination no_of_pages={no_of_pages} changePage={this.changePage}/>;
        }

        var subjects_table;
        if (subjects_data === undefined) {
            //@TODO: show a "loading" animation
        }
        else if (row_count === 0) {
            subjects_table = <div>There is no data to display. If you think this is an error please contact your support personnel.</div>;
        }
        else {
            subjects_table = (
                <div className="table-responsive">
                    <table id="technician-table" className="table borderless">
                    <thead>
                        <tr> {table_columns} </tr>
                    </thead>
                    <tbody id="technician-table-body">
                        {table_rows}
                    </tbody>
                    </table>
                </div>
            );
        }

    return (
        <div className="row">
            {subjects_table}
            {pagination}
        </div>
    );
  }
});


var EventsTable = React.createClass({
    getInitialState: function() {
        return {
            list_of_events: []
        };
    },

    componentDidMount: function() {
        // $('[data-toggle="tooltip"]').tooltip()
    },
    componentWillReceiveProps: function(nextProps) {
        // console.log("componentWillReceiveProps: " + nextProps);
    },
    componentWillMount: function() {
        var _this = this;
        var url = "/api/list_subject_events";
        var request_data = {
            subject_id: this.props.subjectEntity.id
        };

        var request = Utils.api_post_json(url, request_data);
        request.success( function(json) {
            _this.setState({
                list_of_events: json.data.subject_events
            });
            $(".sortable").tablesorter();
        });
        request.fail(function (jqXHR, textStatus, error) {
            console.log('Failed: ' + textStatus + error);
        });
    },

    render: function() {
        var rows = [];
        var _this = this;
        var rowCount = this.state.list_of_events.length,
            eventsData = this.state.list_of_events;

        this.state.list_of_events.map(function(record, i) {
            var eventSelected = _this.props.eventSelected.bind(null, record);
            var title = "Files: " + record.file_names;

            rows.push(
            <tr>
                <td> {record.redcap_arm} </td>
                <td> {record.day_offset} </td>
                <td> {record.redcap_event} </td>
                <td>
                    <button
                        className="btn btn-primary btn-block"
                        data-toggle="tooltip"
                        title={title}
                        onClick={eventSelected}>
                        View {record.total_files} file(s)
                    </button>
                </td>
            </tr>
            );
        });

        var eventsTable;
        if (eventsData === undefined) {
            //@TODO: show a "loading" animation
        }
        else if (rowCount === 0) {
            eventsTable = <div>There is no data to display. If you think this is an error please contact your support personnel.</div>;
        }
        else {
            eventsTable = (
            <div className="table-responsive">
                <table id="event-table" className="table borderless sortable tablesorter">
                    <thead>
                        <tr>
                            <th> REDCap Arm </th>
                            <th> Day Offset </th>
                            <th> REDCap Event </th>
                            <th> File Count </th>
                        </tr>
                    </thead>
                    <tbody id="subject-table-body">
                        {rows}
                    </tbody>
                </table>
            </div>
            );
        }
        return eventsTable;
    }
});

var FilesList = React.createClass({
    getInitialState: function() {
        return {
            list_of_files: []
        };
    },

    componentWillMount: function() {
        var _this = this;
        var request_data = {
            subject_id: this.props.subjectEntity.id,
            event_id: this.props.eventEntity.id
        };

        var request = Utils.api_post_json("/api/list_subject_event_files", request_data);

        request.success(function(json) {
            _this.setState({
                list_of_files: json.data.subject_event_files
            });
        });
        request.fail(function (jqXHR, textStatus, error) {
            console.log('Failed: ' + textStatus + error);
        });
    },
    render: function() {
        return (
        <div className="table-responsive" >
            <table id="technician-table" className="table borderless">
                <thead>
                    <tr>
                        <th className="text-center"> File Name </th>
                        <th className="text-center"> File Size (MB)</th>
                        <th className="text-center"> Uploaded </th>
                        <th className="text-center"> Uploaded By </th>
                        <th className="text-center"></th>
                    </tr>
                </thead>
                <tbody id="technician-table-body">
                {
                this.state.list_of_files.map(function(record, i) {
                    return (<tr>
                        <td>{record.file_name}</td>
                        <td>{(record.file_size / (1024 * 1024)).toFixed(2)}</td>
                        <td>{record.uploaded_at}</td>
                        <td>{record.user_name}</td>
                        <td>
                            <form method="POST" action="/api/download_file">
                                <input type="hidden" name="file_id" value={record.id} />
                                <button className="btn btn-primary">Download File</button>
                            </form>
                        </td>
                    </tr>);
                })}
                </tbody>
            </table>
        </div>
        );
    }
});

var SubjectsPagination = React.createClass({
    getInitialState: function() {
        return {
            no_of_pages: this.props.no_of_pages,
            current_page: 1
        };
    },
    componentWillReceiveProps: function(nextProps) {
        this.setState({
            no_of_pages: nextProps.no_of_pages,
            current_page: this.state.current_page
        });
    },
    activateOnClick: function(i) {
        this.setState({
            no_of_pages: this.state.no_of_pages,
            current_page: i
        });
        this.props.changePage(i);
    },
    nextPage: function() {
        var current_page = this.state.current_page;
        if (current_page === this.state.no_of_pages) {
            return;
        }
        else {
            this.setState({
                no_of_pages: this.state.no_of_pages,
                current_page: current_page+1
            });
            this.props.changePage(current_page + 1);
        }
    },
    prevPage: function() {
        var current_page = this.state.current_page;
        if (current_page === 1) {
            return;
        }
        else {
            this.setState({
                no_of_pages: this.state.no_of_pages,
                current_page: current_page - 1
            });
            this.props.changePage(current_page-1);
        }
    },
    render: function() {
        var pages = [];

        for(var i = 1; i <= this.state.no_of_pages; i++) {
            if(i === this.state.current_page) {
                pages.push(<li className="active"><a>{i}</a></li>);
            }
            else {
                pages.push(<li><a onClick={this.activateOnClick.bind(null, i)}>{i}</a></li>);
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


var Dashboard = React.createClass({
        getInitialState: function() {
        //Add Listner for the url change
        window.onhashchange = this.urlChanged;

        var tabs = [
            "Subjects",
            "Subject Events",
            "Subject Event Files"
        ];
        return {
            current_tab: 0,
            tabs: tabs,
            subjectEntity: "",
            eventEntity: ""
        };
    },
    changeTab: function(i) {
        this.setState({
            current_tab: i
        });
    },
    subjectSelected: function(subjectEntity) {
        this.setState({
            current_tab: 1,
            subjectEntity: subjectEntity
        });
    },
    eventSelected: function(eventEntity) {
        this.setState({
            current_tab: 2,
            eventEntity: eventEntity
        });
    },
    showFiles: function() {
        this.setState({
            current_tab: 3
        });
    },

    urlChanged: function() {
      var hash_value = location.hash;
      var current_tab = this.state.current_tab;

      //check whether the current state is not equal to hash value
      if("#"+this.state.tabs[current_tab] !== hash_value) {

        // State has to be changed
        if(hash_value === "#Subjects") {
          this.setState({
              current_tab: 0,
              eventEntity: ""
          });
        }
        else if (hash_value === "#Events" && this.state.current_tab === 2) {
          // The condition 'this.state.current_tab==2' is to avoid
          // state changes for forward button click from subjects tab
          this.setState({current_tab: 1});
        }
      }
    },
    render: function() {
        var visible_tab,
            selected_subject_id,
            selected_event_id;
        var breadcrumbs = [];
        var current_tab = this.state.current_tab;
        var tabs = this.state.tabs;

        for(var i = 0; i < tabs.length; i++) {
            var tab_class;
            if(current_tab === i) {
                breadcrumbs.push(<li><a>{tabs[i]}</a></li>);
            }
            else if(current_tab > i) {
                breadcrumbs.push(
                        <li className="prev-page" onClick={this.changeTab.bind(null, i)}>
                        <a>{tabs[i]}</a>
                        </li>);
            }
            else if(current_tab < i) {
                breadcrumbs.push(<li className="next-page"><a>{tabs[i]}</a></li>);
            }
        }

        $("#upload-files").hide();
        $("#upload-complete-button").hide();

        if (current_tab === 0) {
            window.location.hash = 'Subjects';
            visible_tab = <SubjectsTable subjectSelected = {this.subjectSelected} />;
        }
        else if (current_tab === 1) {
            selected_subject_id = "Subject ID: " + this.state.subjectEntity.redcap_id;
            selected_event_id = "";
            window.location.hash = 'Events';
            visible_tab = <EventsTable subjectEntity = {this.state.subjectEntity} eventSelected = {this.eventSelected}/>;
        }
        else if (current_tab === 2) {
            selected_subject_id = "Subject ID: " + this.state.subjectEntity.redcap_id;
            selected_event_id = "Event: " + this.state.eventEntity.redcap_arm + " " + this.state.eventEntity.redcap_event;
            window.location.hash = 'Files';
            visible_tab = <FilesList subjectEntity = {this.state.subjectEntity} eventEntity = {this.state.eventEntity}/>;
        }

        return (
            <div>
                <div className="panel-heading">
                    <div id="crumbs">
                        <ul>
                            {breadcrumbs}
                        </ul>
                    </div>
                </div>
                <div className="row">
                <div className="col-md-offset-4 col-md-4 col-xs-12">
                <table id="technician-table" className="table borderless">
                    <thead>
                    <tr>
                        <th>{selected_subject_id}</th>
                        <th>{selected_event_id}</th>
                     </tr>
                </thead>
                </table>
                </div>
                </div>
                <div className="panel-body">
                    {visible_tab}
                </div>
            </div>
        );
    }
});

React.render(<Dashboard/>, document.getElementById("dashboard"));
