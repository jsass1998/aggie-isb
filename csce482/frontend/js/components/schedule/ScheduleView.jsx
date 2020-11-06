import React, {Component} from "react";
import TimeGrid from "./TimeGrid";
import PopUpDialog from "../PopUpDialog";
import {create_schedule_tooltip} from "../../utils/constants";
import SidePanel from "./SidePanel";

class ScheduleView extends Component {
  constructor(props) {
    super(props);
    this.state = {
      hideToolTips: props.hideToolTips,
      showCourseSelection: false,
      showSidePanel: true,
    };
  }

  handleCheckChanged(checked) {
    localStorage.setItem('hideToolTips', checked ? '1' : '0');
  }

  generateSchedules(schedules) {
    console.log('courses to add', schedules);
    // Here we would send a request to the backend to generate schedules and handle the response.
  }

  render() {
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
          courseList={this.props.courseList}
          generateSchedules={this.generateSchedules}
        />
        <TimeGrid />
      </div>
    );
  }
}

export default ScheduleView;