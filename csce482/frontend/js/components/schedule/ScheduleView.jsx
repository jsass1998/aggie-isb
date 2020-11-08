import React, {Component} from "react";
import TimeGrid from "./TimeGrid";
import PopUpDialog from "../PopUpDialog";
import {create_schedule_tooltip} from "../../utils/constants";
import SidePanel from "./SidePanel";
import {weekdayMap} from "../../utils/constants";
import axios from "axios";
import Cookies from 'js-cookie';
import CircularProgress from "@material-ui/core/CircularProgress";

class ScheduleView extends Component {
  constructor(props) {
    super(props);

    this.eventRef = React.createRef();
    this.gridUpdateTimer = null;
    this.onGridUpdated =  this.onGridUpdated.bind(this);

    this.state = {
      csrfToken: Cookies.get('csrftoken'),
      currentUser: null,
      courseList: [],
      semesterList: [], // Currently not used
      selectedSemester: '',
      selectedCourses: [],
      scheduleList: [],
      userActivity: [], // A list of activity instances where each instance is a list with day, start & end times (string format)
      gridInstances: [], // TimeGrid schedule state
      hideToolTips: props.hideToolTips,
      showCourseSelection: false,
      showSidePanel: true,
    };
  }

  componentDidMount() {
    // this.fetchCourseData();
    this.fetchUser();
  }

  // TODO -  refactor to get user based off of google auth data (if browser is signed in)
  fetchUser() {
    axios.get('api/users/2/').then(res => {
      this.setState({
        currentUser: res.data,
      });
    });
  }

  fetchCourseData(semesterString) {
    let semester = semesterString.split('-');
    axios.get(`api/courses/?term=${semester[0].replace(' ', '%20')}`).then(res => {
      console.log('course list', res.data);
      this.setState({
        courseList: res.data,
      });
    });
  }

  handleCheckChanged(checked) {
    localStorage.setItem('hideToolTips', checked ? '1' : '0');
  }

  // TODO: Watch out for when activities are programmatically added to grid
  //  - not currently handled
  onGridUpdated(params) {
    // console.log('1');
    let updatedUserActivity = [];

    params.forEach(activityInstance => {
      updatedUserActivity.push([
        weekdayMap[activityInstance[0].getDay()],
        activityInstance[0].toString().split(' ')[4],
        activityInstance[1].toString().split(' ')[4],
      ]);
    });

    // BE VERY CAREFUL ADJUSTING HOW THE `TimeGrid` STATE IS UPDATED
    // IF YOU DO SOMETHING WRONG YOU WILL CREATE AN INFINITE LOOP AND
    // LOCK THE WEBPAGE
    this.setState({
      gridInstances: params,
      userActivity: updatedUserActivity,
    });
  };

  onSemesterUpdated(selectedSemester) {
    this.setState({
      selectedSemester: selectedSemester.split('-')[0],
    });
  }

  onCourseListUpdated(courses) {
    let newSelectedCourses = [];
    courses.forEach(course => {
      newSelectedCourses.push(course.course_id);
    });
    this.setState({
      selectedCourses: newSelectedCourses,
    });
  }

  generateSchedules() {
    // console.log('courses to add', this.state.selectedCourses);
    // console.log('userActivity', this.state.userActivity);
    // Here we would send a request to the backend to generate schedules and handle the response.
    axios.post('api/generate_schedules/',
      {
        csrfmiddlewaretoken: this.state.csrfToken,
        user_id: this.state.currentUser.id,
        term: this.state.selectedSemester,
        courses: this.state.selectedCourses,
        blocked_times: this.state.userActivity
      },
      {
        headers: {
          'X-CSRFToken': this.state.csrfToken,
        }
      }).then(res => {
        console.log(res);
    }).catch(err => {
      console.error(err);
    });
  }

  render() {
    if (!this.state.currentUser) {
      return (
        <div>
          <div className={'loading-wheel'}>
            <CircularProgress/>
            <div>Loading...</div>
          </div>
        </div>
      );
    }
    return(
      <div>
        <PopUpDialog
          active={!this.state.hideToolTips}
          title='Create a Schedule'
          message={create_schedule_tooltip}
          onClose={() => this.setState({hideToolTips: true})}
          showCheckbox={true}
          checkboxText={"Don't show again"}
          handleCheckChanged={this.handleCheckChanged}
        />
        <SidePanel
          courseList={this.state.courseList}
          fetchCourses={this.fetchCourseData.bind(this)}
          scheduleList={this.state.scheduleList}
          onSemesterUpdated={this.onSemesterUpdated.bind(this)}
          onCourseListUpdated={this.onCourseListUpdated.bind(this)}
          generateSchedules={this.generateSchedules.bind(this)}
        />
        <TimeGrid
          ref={this.eventRef}
          schedule={this.state.gridInstances}
          handleGridChange={this.onGridUpdated}
        />
      </div>
    );
  }
}

export default ScheduleView;