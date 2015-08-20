// Implements react componenst:
//  AdminUsersRow - ...
//  AdminUsersTable - ...
//  AdminUsersPagination - ..
//  AddNewUserForm - ...

var AdminUsersRow = React.createClass({
    getInitialState: function() {
        return {
            record: this.props.record,
            row_num: this.props.row_num
        };
    },
    componentWillReceiveProps: function(nextProps) {
        this.setState({
            record: nextProps.record,
            row_num: nextProps.row_num
        });
    },
    sendEmailVerification: function() {
        var record = this.state.record;
        var data = {
            "user_id": record.id
        };
        var request = Utils.api_post_json("/api/send_verification_email", data);

        request.success( function(json) {
            if(json.status === "success") {
                $("#show-message").text("Verification Email Sent")
                                  .show().delay(1000).fadeOut('slow');
            }
            else {
                $("#show-message").text("Failed.Try Again")
                                  .show().delay(1000).fadeOut('slow');
            }
        });
        request.fail(function (jqXHR, textStatus, error) {
            $("#show-message").text("There was a problem with the request. Please try again.")
                              .show().delay(1000).fadeOut('slow');
        });
    },

    deactivateAccount: function() {
        var record = this.state.record;
        var _this = this;
        var data = {
            "user_id": record.id
        }
        var request = Utils.api_post_json("/api/deactivate_account", data);
        request.success( function(json) {
            if(json.status === "success") {
                record.is_active = false;
                $("#show-message").text("Account Deactivated")
                                  .show().delay(1000).fadeOut('slow');
                _this.setState({record: record});
            }
            else {
                $("#show-message").text("There was a problem with the request. Please try again.")
                                  .show().delay(1000).fadeOut('slow');
            }
        });
        request.fail(function (jqXHR, textStatus, error) {
            $("#show-message").text("There was a problem with the request. Please try again.")
                              .show().delay(1000).fadeOut('slow');
        });
    },

    activateAccount: function(){
        var record = this.state.record;
        var _this = this;
        var data = {
            "user_id": record.id
        };
        var request = Utils.api_post_json("/api/activate_account", data);

        request.success( function(json) {
            if(json.status === "success") {
                record.is_active = true;
                $("#show-message").text("Account Activated ")
                                  .show().delay(1000).fadeOut('slow');
                _this.setState({record: record});
            }
            else {
                $("#show-message").text("Failed.Try Again")
                                  .show().delay(1000).fadeOut('slow');
            }
        });
        request.fail(function (jqXHR, textStatus, error) {
            $("#show-message").text("Failed to Send Request.Try Again")
                              .show().delay(1000).fadeOut('slow');
        });
    },

    extendExpirationDate: function() {
        var record = this.state.record;
        var _this = this;
        var data = {
            "user_id": record.id};
        var request = Utils.api_post_json("/api/extend_account", data);

        request.success( function(json) {
            if(json.status === "success") {
                record.is_expired = false;
                $("#show-message").text("Expiration Date Extended")
                                  .show().delay(1000).fadeOut('slow');
                _this.setState({record: record});
            }
            else {
                $("#show-message").text("Failed.Try Again")
                                  .show().delay(1000).fadeOut('slow');
            }
        });
        request.fail(function (jqXHR, textStatus, error) {
            $("#show-message").text("Failed to Send Request.Try Again")
                              .show().delay(1000).fadeOut('slow');
        });
    },
    expireAccount: function() {
        var record = this.state.record;
        var _this = this;
        var data = {"user_id": record.id};
        var request = Utils.api_post_json("/api/expire_account", data);

        request.success( function(json) {
            if(json.status == "success") {
                record.is_expired = true;
                $("#show-message").text("Account Expired Successfully ")
                                  .show().delay(1000).fadeOut('slow');
                _this.setState({record: record});
            }
            else {
                $("#show-message").text("Failed.Try Again")
                                  .show().delay(1000).fadeOut('slow');
            }
        });
        request.fail(function (jqXHR, textStatus, error) {
            $("#show-message").text("Failed to Send Request.Try Again")
                              .show().delay(1000).fadeOut('slow');
        });
    },
    render: function() {
            var record = this.state.record;
            var row_num = this.state.row_num;
            var roles,
                emailButton,
                expireButton,
                deactivateButton,
                title = "",
                display = "",
                expirationDate = record.access_expires_at;

            if (record.roles) {
                roles = record.roles.join("<br>");
            }
            if (record.email_confirmed_at) {
                emailButton = <div> {record.email_confirmed_at} </div>;
            }
            else {
                emailButton = <button
                    className="btn btn-primary"
                    data-toggle="tooltip"
                    data-placement="top"
                    title="Send Verification Email"
                    onClick={this.sendEmailVerification}>
                        <i className="fa fa-envelope-o">
                        </i>
                    </button>;
            }

            if (record.is_expired) {
                title = "Extend access by 180 days (expired " + expirationDate + ")";
                expireButton = <div>
                    <button
                        className="btn btn-primary"
                        data-toggle="tooltip"
                        title={title}
                        onClick={this.extendExpirationDate}>
                        Extend
                    </button>
                    </div>
            }
            else {
                title = "Expire Now (current expiration date: " + expirationDate + ")";
                expireButton = <button
                    className="btn btn-primary"
                    data-toggle="tooltip"
                    title={title}
                    onClick={this.expireAccount}>
                        Expire
                    </button>
            }
            if (record.is_active) {
                deactivateButton = <button
                    className="btn btn-primary"
                    data-toggle="tooltip"
                    title="Deactivate Now"
                    onClick={this.deactivateAccount}>
                        Deactivate
                    </button>
            }
            else {
                deactivateButton = <button
                    className="btn btn-primary"
                    data-toggle="tooltip"
                    title="Activate Now"
                    onClick={this.activateAccount}>
                        Activate
                    </button>
            }

            return (<tr>
                            <td className="text-right">{record.id}</td>
                            <td className="text-left">{record.email}</td>
                            <td className="text-left">{record.first}</td>
                            <td className="text-left">{record.last}</td>
                            <td className="text-left" dangerouslySetInnerHTML={{__html:roles}}></td>
                            <td className="text-left">{record.added_at}</td>
                            <td className="text-left">{emailButton}</td>
                            <td className="text-center">{expireButton}</td>
                            <td className="text-center">{deactivateButton}</td>
                        </tr>
            );
    }
});

var AdminUsersTable = React.createClass({
    getInitialState: function() {
        return {
            list_of_users: this.props.list_of_users
        };
    },
    componentDidMount: function() {
        $('[data-toggle="tooltip"]').tooltip()
    },
    componentWillReceiveProps: function(nextProps) {
        this.setState({list_of_users: nextProps.list_of_users});
    },
    render: function() {
        var rows = [];
        this.state.list_of_users.map(function(record, i) {
            rows.push(
                <AdminUsersRow record={record} row_num={i+1} key={i} />
            );
        });

        return (
    <div className="table-responsive">
        <table className="table borderless sortable">
            <thead>
                <tr>
                    <th className="text-right">User ID</th>
                    <th className="text-center">User Email</th>
                    <th className="text-center">First </th>
                    <th className="text-center">Last </th>
                    <th className="text-center">Role</th>
                    <th className="text-center">Date Added</th>
                    <th className="text-center">Email Verified</th>
                    <th className="text-center">Account Expiration</th>
                    <th className="text-center">Account Status</th>
                </tr>
            </thead>
            <tbody>
                { rows }
            </tbody>
        </table>
    </div>
    );
  }
});

var AdminUsersPagination = React.createClass({
    getInitialState: function() {
        return {
            total_pages: this.props.total_pages,
            current_page: 1
        };
    },
    componentWillReceiveProps: function(nextProps) {
        this.setState({
            total_pages: nextProps.total_pages,
            current_page: this.state.current_page
        });
    },
    activateOnClick: function(i) {
        this.setState({total_pages: this.state.total_pages, current_page: i});
        this.props.changePage(i);
    },
    nextPage: function() {
        var current_page = this.state.current_page;
        if(current_page === this.state.total_pages) {
            return;
        }
        else {
            this.setState({total_pages: this.state.total_pages, current_page: current_page + 1});
            this.props.changePage(current_page + 1);
        }
    },
    prevPage: function() {
        var current_page = this.state.current_page;
        if (current_page === 1) {
            return;
        }
        this.setState({
            total_pages: this.state.total_pages,
            current_page: current_page - 1
        });
        this.props.changePage(current_page-1);
    },
    render: function() {
        var pages = [];
        for (var i = 1; i <= this.state.total_pages; i++) {
            if (i === this.state.current_page) {
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


var AddNewUserForm = React.createClass({
    getInitialState: function() {
        return {error: ""};
    },

    clearError: function() {
        this.setState({error: ""});
    },

    addUser: function() {
        //Get the values entered by the user in the form
        var usrEmail = this.refs.user_email.getDOMNode().value.trim();
        var usrFirst = this.refs.user_first_name.getDOMNode().value.trim();
        var usrMI = this.refs.user_middle_name.getDOMNode().value.trim();
        var usrLast  = this.refs.user_last_name.getDOMNode().value.trim();
        var roles = [];

        // https://developer.mozilla.org/en-US/docs/Web/API/HTMLOptionsCollection
        // https://github.com/facebook/react/blob/057f41ec0f01e5e716358ad18cf7166d5cc00d68/src/browser/ui/dom/components/__tests__/ReactDOMSelect-test.js
        var collection = this.refs.user_roles.getDOMNode().options;

        for (var i = 0; i < collection.length; i++) {
            if (collection.item(i).selected) {
                roles.push(collection.item(i).value);
            }
        }
        console.log("roles: " + roles);

        if (usrEmail === "") {
            this.setState({error: "Email cannot be empty."});
            return;
        }

        if(! Utils.validate_email(usrEmail)) {
            this.setState({error: "Invalid email address."});
            return;
        }
        if (usrFirst === "") {
            this.setState({error: "First name cannot be empty."});
            return;
        }
        if (usrLast == "") {
            this.setState({error: "Last name cannot be empty."});
            return;
        }
        if (usrMI.length > 1) {
            this.setState({error: "Middle name should be one character long."});
            return;
        }

        if (roles.length < 1) {
            this.setState({error: "Please select at least one role for this user."});
            return;
        }

        var data = {
            "email"     : usrEmail,
            "first"     : usrFirst,
            "minitial"  : usrMI,
            "last"      : usrLast,
            "roles[]"   : roles
        };

    console.log('sending data: ' + Utils.print_r(data));

    var request = Utils.api_post_json("/api/save_user", data);
    var _this = this;

    request.success( function(json) {
        console.log("got back: " + JSON.stringify(json));

        if(json.status === "success") {
            var record = json.data.user;
            if (record) {
                var data = {
                    'id'            : record.id,
                    'email'         : record.email,
                    'first'         : record.first,
                    'last'          : record.last,
                    'minitial'      : record.minitial,
                    'added_at'      : record.added_at,
                    'access_expires_at': record.access_expires_at,
                    'email_confirmed_at': record.email_confirmed_at,
                    'is_active'     : record.is_active,
                    'roles'         : record.roles
                };
                _this.props.addNewUser(data);
            }
        }
        else {
            _this.setState({error: json.data.message});
            return;
        }
    });

    request.fail(function (jqXHR, textStatus, error) {
        console.log('Failed: ' + textStatus + error);
        _this.setState({
            error: "There was some unknown error. Please try again."});
        return;
    });
  },
  render: function() {
    var error;

    // Add generic function for displaying errors
    if (this.state.error !== "") {
      error = <div className="alert alert-danger alert-dismissible">
              <button type="button" onClick={this.clearError} className="close">&times;</button>
              {this.state.error}
            </div>
    }

    return (
<div className="col-sm-offset-3 col-sm-6">

    {error}

    <div className="form-horizontal">
        <h4> Please enter user details </h4>
        <div className="form-group">
            <label for="id-user-email" className="col-sm-4 control-label">Email</label>
            <div className="col-sm-8">
                <input type="email" className="form-control" id="id-user-email" ref="user_email" placeholder="Email" />
            </div>
        </div>
        <div className="form-group">
            <label for="id-user-first" className="col-sm-4 control-label">First Name</label>
            <div className="col-sm-8">
                <input type="text" className="form-control" id="id-user-first" ref="user_first_name" placeholder="First Name" />
            </div>
        </div>
        <div className="form-group">
            <label for="id-user-mi" className="col-sm-4 control-label">Middle Name</label>
            <div className="col-sm-8">
                <input type="text" className="form-control" id="id-user-mi" ref="user_middle_name" placeholder="Middle Name" />
            </div>
        </div>
        <div className="form-group">
            <label for="id-user-last" className="col-sm-4 control-label">Last Name</label>
            <div className="col-sm-8">
                <input type="text" className="form-control" id="id-user-last" ref="user_last_name" placeholder="Last Name" />
            </div>
        </div>
        <div className="form-group">
            <label for="id-user-roles" className="col-sm-4 control-label">Roles</label>
            <div className="col-sm-8">
              <select ref="user_roles" className="form-control" id="id-user-roles" multiple={true}>
                  <option value="admin">Admin</option>
                  <option value="technician">Technician</option>
                  <option value="researcher_one">Researcher 1</option>
                  <option value="researcher_two">Researcher 2</option>
                </select>
            </div>
        </div>
        <div className="form-group">
            <div className="col-sm-offset-2 col-sm-10">
                <button onClick={this.addUser} className="btn btn-danger">Save User</button>
            </div>
        </div>
    </div>
</div>
    )
  }

});

var AdminUserManagement = React.createClass({
    getInitialState: function() {
        return {
            list_of_users: undefined,
            total_pages: 1,
            show_user_form: false,
            error: ""
        };
    },
    componentWillMount: function() {
        this.changeData(1);
        /*
        var request_data = { "per_page": "10", "page": "1" };
        var request = Utils.api_post_json("/api/list_users", request_data);
        var _this = this;

        request.success( function(json) {
            if (json.status === "success") {
                var state = {
                    list_of_users: json.data.list_of_users,
                    total_pages: json.data.total_pages
                }
                _this.setState(state);
            }
            else {
                _this.setState({
                    list_of_users: [],
                    total_pages: this.state.total_pages,
                    show_user_form: false,
                    error: json.data.message
                });
            }
        });
        request.fail(function (jqXHR, textStatus, error) {
            console.log('Failed: ' + textStatus + error);
        });
        */
    },
    changePage: function(pageNum) {
        this.changeData(pageNum);
    },
    changeData: function(pageNum) {
        var request_data = {'per_page': 25, 'page_num': pageNum};
        var _this = this;
        var request = Utils.api_post_json("/api/list_users", request_data);

        request.success( function(json) {
            if (json.status === "success") {
                var state = {
                    list_of_users: json.data.list_of_users,
                    total_pages: json.data.total_pages
                }
                _this.setState(state);
                $(".sortable").tablesorter();
            }
            else {
                _this.setState({
                    list_of_users: [],
                    total_pages: this.state.total_pages,
                    show_user_form: false,
                    error: json.data.message
                });
            }
        });
        request.fail(function (jqXHR, textStatus, error) {
            console.log('Failed: ' + textStatus + error);
        });
    },

    addNewUser: function(data) {
        var list_of_users = this.state.list_of_users;
        list_of_users.unshift(data);
        console.log(list_of_users);

        this.setState({
            list_of_users: list_of_users,
            total_pages: this.state.total_pages,
            show_user_form: false
        });
    },

    toggleAddUserForm: function() {
        //change the bool value of show_user_form variable to opposite
        var show_user_form = !this.state.show_user_form;
        this.setState({
            list_of_users   :  this.state.list_of_users,
            total_pages     :  this.state.total_pages,
            show_user_form  :  show_user_form
        });
    },
    render: function() {
        var total_pages = this.state.total_pages;
        var list_of_users = this.state.list_of_users;
        var pagination;
        var show_user_form;
        var button_text = "Open 'Add User' Form";

        if(total_pages > 1) {
            pagination = <AdminUsersPagination total_pages={total_pages} changePage={this.changePage}/>;
        }

        if(this.state.show_user_form) {
            button_text = "Close 'Add User' Form";
            show_user_form = <AddNewUserForm addNewUser = {this.addNewUser}/>
        }

        var users_table;

        if(list_of_users === undefined) {
            //@TODO: show a "loading" animation
        }
        else if(this.state.error !== "") {
            users_table = <div className="alert alert-danger">There was an error loading the information: {this.state.error}. Please contact your support personnel.</div>
        }
        else if (list_of_users.length === 0) {
            users_table = <div>There is no data to display. If you think this is an error please contact your support personnel.</div>;
        }
        else {
            users_table = <AdminUsersTable list_of_users={this.state.list_of_users}/>
        }
        return (
                <div>
        <button onClick={this.toggleAddUserForm} className="btn btn-danger">{button_text}</button>
        <br/>
        <div className="row">
          {show_user_form}
        </div>
        <div className="row">
          <br/>
          {users_table}
          {pagination}
        </div>
    </div>
    );
  }
});
React.render(<AdminUserManagement/>, document.getElementById("admin-user-managememt"));
