import React, {Component} from "react";
import TimeGrid from "./TimeGrid";
import PopUpDialog from "../PopUpDialog";
import {create_schedule_tooltip} from "../../utils/constants";
import SidePanel from "./SidePanel";
import axios from "axios";
import CircularProgress from "@material-ui/core/CircularProgress";

class ScheduleView extends Component {
  constructor(props) {
    super(props);
    this.state = {
      courseList: [],
      scheduleList: [],
      hideToolTips: props.hideToolTips,
      showCourseSelection: false,
      showSidePanel: true,
    };
  }

  componentDidMount() {
    this.fetchCourseData().then(r => {});
  }

  async fetchCourseData() {
    let res = await axios.get('api/courses/');
    this.setState({
      courseList: res.data,
    });
  }

  handleCheckChanged(checked) {
    localStorage.setItem('hideToolTips', checked ? '1' : '0');
  }

  generateSchedules(schedules) {
    console.log('courses to add', schedules);
    // Here we would send a request to the backend to generate schedules and handle the response.
  }

  render() {
    if (!this.state.courseList)
      return (
        <div>
          <div className={'loading-wheel'}>
            <CircularProgress />
            <div>Loading...</div>
          </div>
        </div>
      );
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
          scheduleList={this.state.scheduleList}
          generateSchedules={this.generateSchedules}
        />
        <TimeGrid />
      </div>
    );
  }
}

export default ScheduleView;