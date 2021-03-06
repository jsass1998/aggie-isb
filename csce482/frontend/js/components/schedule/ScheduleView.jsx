import React, {Component} from "react";
import {ScheduleContext} from "./ScheduleContext";
import TimeGrid from "./TimeGrid";
import PopUpDialog from "../PopUpDialog";
import {create_schedule_tooltip} from "../../utils/constants";
import SidePanel from "./SidePanel";
import {weekdayMap, dayToDateMap} from "../../utils/constants";
import axios from "axios";
import Cookies from 'js-cookie';
import CircularProgress from "@material-ui/core/CircularProgress";
import {toast, ToastContainer} from "react-toastify";
import 'react-toastify/dist/ReactToastify.css';

class ScheduleView extends Component {
  constructor(props) {
    super(props);

    this.onGridUpdated =  this.onGridUpdated.bind(this);

    this.state = {
      csrfToken: Cookies.get('csrftoken'),
      currentUser: null,
      crnList: [],
      creditHourCount: null,
      courseList: [],
      semesterList: [], // List term dicts containing time & location (i.e. 'FALL 2020' and 'College Station'
      selectedSemester: '',
      selectedCampus: '',
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
    this.fetchUser(this.props.userEmail);
    this.fetchTermData();
  }

  // Re-render when user signs in BUGGED IMPLEMENTATION, revisit later? Maybe try componentDidUpdate()
  // shouldComponentUpdate(nextProps, nextState, nextContext) {
  //   console.log('shouldComponentUpdate', this.props, nextProps);
  //   return this.props.userEmail != nextProps.userEmail;
  // }

  // TODO -  need to call after user signs in, not just when component loads
  fetchUser(userEmail) {
    if (userEmail)
      axios.get(`api/users/?email=${userEmail.replace('@', '%40').replace('.', '%2e')}`).then(res => {
        this.setState({
          currentUser: res.data[0],
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
    const url = `api/courses/?term=${semester[0].replace(' ', '%20')}&campus=${semester[1].replace(' ', '%20')}`;
    axios.get(url).then(res => {
      this.setState({
        courseList: res.data,
      });
    });
  }

  fetchUserSchedules(semesterString) {
    if (this.state.currentUser) {
      let semester = semesterString.split('-');
      const url = `api/schedules/?user=${this.state.currentUser.id}&term=${semester[0].replace(' ', '%20')}&campus=${semester[1].replace(' ', '%20')}`;
      axios.get(url).then(res => {
        this.setState({
          scheduleList: res.data,
        })
      });
    }
  }

  isWaitingForUser() {
    return this.userEmail && !this.state.currentUser;
  }

  handleCheckChanged(checked) {
    localStorage.setItem('hideToolTips', checked ? '1' : '0');
  }

  getEventInfo(dateRange) {
    let eventKey = `${weekdayMap[dateRange[0].getDay()]}-${dateRange[0].toString().split(' ')[4]}-${dateRange[1].toString().split(' ')[4]}`;
    return this.state.gridInstanceDataDict[eventKey];
  }

  loadSchedule(activities) {
    let newGridInstances = [];
    let newGridInstanceDataDict = {};

    // Things to update state
    let crnList = [];
    let creditHourCount = 0;

    activities.forEach(activity => {
      if (activity.section)
        crnList.push(activity.section.crn);
      creditHourCount += activity.section ? activity.section.credit_hours : 0;

      // Convert each activity instance into a gridInstance and generate it's key-value pair for the gridInstanceDataDict
      for (let i = 0; i < activity.activity_instance_set.length; i++) {
        let aInstance = activity.activity_instance_set[i];
        let startDate = new Date()
          startDate.setTime(Date.parse(`${dayToDateMap[aInstance.day]}T${aInstance.starttime}`));
        let endDate = new Date()
          endDate.setTime(Date.parse(`${dayToDateMap[aInstance.day]}T${aInstance.endtime}`));
        let instance = [startDate, endDate];
        let dictKey = `${aInstance.day}-${aInstance.starttime}-${aInstance.endtime}`;
        let data = {
          title: activity.title,
          timeRange: '',
          location: aInstance.location,
        }
        newGridInstances.push(instance);
        newGridInstanceDataDict[dictKey] = data;
      }
    });

    this.setState({
      crnList: crnList,
      creditHourCount: creditHourCount,
      gridInstanceDataDict: newGridInstanceDataDict,
    }, () => this.onGridUpdated(newGridInstances, true));
  }

  // TODO: Watch out for when activities are programmatically added to grid vs manually added
  //  - not currently handled well
  /**
   * Takes a list of lists where the inner list contains two Date objects
   * representing the start and end time of a particular activity.
   *
   * This function is used both to handle updating the grid state upon
   * user interacts as well as to programmatically load generated schedules
   * **/
  onGridUpdated(params, isLoadOperation=false) {
    let updatedUserActivity = [];
    let updatedDataDict = this.state.gridInstanceDataDict;

    // Only write to dict & update if user is manually adding to grid
    if (!isLoadOperation)
      params.forEach(activityInstance => {
        // Add the dict key to the user activity list
        updatedUserActivity.push([
          weekdayMap[activityInstance[0].getDay()],
          activityInstance[0].toString().split(' ')[4],
          activityInstance[1].toString().split(' ')[4],
        ]);

        // Set key to 'DAY-HH:MM:SS-HH:MM:SS' and data to an object containing a title string and a time range formatted as 'HH:MM-HH:MM'
        updatedDataDict[`${weekdayMap[activityInstance[0].getDay()]}-${activityInstance[0].toString().split(' ')[4]}-${activityInstance[1].toString().split(' ')[4]}`]
          = {
          title: weekdayMap[activityInstance[0].getDay()],
          timeRange: `${activityInstance[0].toString().split(' ')[4].substring(0, 5)}-${activityInstance[1].toString().split(' ')[4].substring(0, 5)}`
        };
      });

    if (!isLoadOperation)
      this.setState({
        gridInstances: params,
        gridInstanceDataDict: updatedDataDict,
        userActivity: updatedUserActivity,
      });
    else
      this.setState({
        gridInstances: params,
      });
  };

  onSemesterUpdated(selectedSemester) {
    this.setState({
      selectedSemester: selectedSemester.split('-')[0],
      selectedCampus: selectedSemester.split('-')[1],
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
    if (!this.state.selectedCourses.length) {
      // TODO: Fix gross styles
      toast.info("You haven't selected any courses!");
      return;
    }

    let reqData = {
      csrfmiddlewaretoken: this.state.csrfToken,
      user_id: this.state.currentUser ? this.state.currentUser.id : null,
      term: this.state.selectedSemester,
      campus: this.state.selectedCampus,
      courses: this.state.selectedCourses,
      blocked_times: this.state.userActivity
    };

    axios.post('api/generate_schedules/', reqData,
      {
        headers: {
          'X-CSRFToken': this.state.csrfToken,
        }
      }).then(res => {
        this.setState({
          scheduleList: res.data,
        })
    }).catch(err => {
      console.error(err);
    });
  }

  render() {
    if (!this.state.semesterList.length || this.isWaitingForUser()) {
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
          fetchUserSchedules={this.fetchUserSchedules.bind(this)}
          scheduleList={this.state.scheduleList}
          onSemesterUpdated={this.onSemesterUpdated.bind(this)}
          onCourseListUpdated={this.onCourseListUpdated.bind(this)}
          generateSchedules={this.generateSchedules.bind(this)}
          loadSchedule={this.loadSchedule.bind(this)}
        />
        <ScheduleContext.Provider value={this.getEventInfo.bind(this)}>
          <TimeGrid
            getEventInfo={this.getEventInfo.bind(this)}
            schedule={this.state.gridInstances}
            handleGridChange={this.onGridUpdated}
          />
        </ScheduleContext.Provider>
        <ToastContainer
          className='toast-pane'
          position="bottom-left"
          autoClose={3000}
          hideProgressBar={false}
          newestOnTop
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
        />
      </div>
    );
  }
}

export default ScheduleView;