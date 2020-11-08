import React, {Component} from "react";
import {ScheduleContext} from "./ScheduleContext";
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

    this.gridUpdateTimer = null;
    this.onGridUpdated =  this.onGridUpdated.bind(this);

    this.state = {
      csrfToken: Cookies.get('csrftoken'),
      currentUser: null,
      courseList: [],
      semesterList: [], // List term dicts containing time & location (i.e. 'FALL 2020' and 'College Station'
      selectedSemester: '',
      selectedCourses: [],
      scheduleList: [],
      userActivity: [], // A list of activity instances where each instance is a list with day, start & end times (string format)
      gridInstances: [], // TimeGrid schedule state
      gridInstanceDataDict: {}, // A gross way to interact with grid EventContent
      hideToolTips: props.hideToolTips,
      showCourseSelection: false,
      showSidePanel: true,
    };
  }

  componentDidMount() {
    this.fetchUser();
    this.fetchTermData();
  }

  // TODO -  refactor to get user based off of google auth data (if browser is signed in)
  fetchUser() {
    axios.get('api/users/2/').then(res => {
      this.setState({
        currentUser: res.data,
      });
    });
  }

  fetchTermData() {
    axios.get('/api/term_locations/').then(res => {
      this.setState({
        semesterList: res.data,
      });
    });
  }

  fetchCourseData(semesterString) {
    let semester = semesterString.split('-');
    axios.get(`api/courses/?term=${semester[0].replace(' ', '%20')}`).then(res => {
      this.setState({
        courseList: res.data,
      });
    });
  }

  handleCheckChanged(checked) {
    localStorage.setItem('hideToolTips', checked ? '1' : '0');
  }

  getEventInfo(dateRange) {
    let eventKey = `${weekdayMap[dateRange[0].getDay()]}-${dateRange[0].toString().split(' ')[4]}-${dateRange[1].toString().split(' ')[4]}`;
    return this.state.gridInstanceDataDict[eventKey];
  }

  // TODO: Watch out for when activities are programmatically added to grid
  //  - not currently handled
  onGridUpdated(params) {
    let updatedUserActivity = [];
    let updatedDataDict = {};

    params.forEach(activityInstance => {
      updatedUserActivity.push([
        weekdayMap[activityInstance[0].getDay()],
        activityInstance[0].toString().split(' ')[4],
        activityInstance[1].toString().split(' ')[4],
      ]);
      updatedDataDict[`${weekdayMap[activityInstance[0].getDay()]}-${activityInstance[0].toString().split(' ')[4]}-${activityInstance[1].toString().split(' ')[4]}`] = weekdayMap[activityInstance[0].getDay()];
    });

    // BE VERY CAREFUL ADJUSTING HOW THE `TimeGrid` STATE IS UPDATED
    // IF YOU DO SOMETHING WRONG YOU WILL CREATE AN INFINITE LOOP AND
    // LOCK THE WEBPAGE
    this.setState({
      gridInstances: params,
      gridInstanceDataDict: updatedDataDict,
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
        console.log(res.data);
    }).catch(err => {
      console.error(err);
    });
  }

  render() {
    if (!this.state.currentUser || !this.state.semesterList.length) {
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
          semesterList={this.state.semesterList}
          fetchCourses={this.fetchCourseData.bind(this)}
          scheduleList={this.state.scheduleList}
          onSemesterUpdated={this.onSemesterUpdated.bind(this)}
          onCourseListUpdated={this.onCourseListUpdated.bind(this)}
          generateSchedules={this.generateSchedules.bind(this)}
        />
        <ScheduleContext.Provider value={this.getEventInfo.bind(this)}>
          <TimeGrid
            getEventInfo={this.getEventInfo.bind(this)}
            schedule={this.state.gridInstances}
            handleGridChange={this.onGridUpdated}
          />
        </ScheduleContext.Provider>
      </div>
    );
  }
}

export default ScheduleView;