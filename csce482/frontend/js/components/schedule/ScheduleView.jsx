import React, {Component, useState} from "react";
import TimeGrid from "./TimeGrid";
import PopUpDialog from "../PopUpDialog";
import {create_schedule_tooltip} from "../../utils/constants";
import Dialog from "@material-ui/core/Dialog";
import {DialogTitle} from "@material-ui/core";
import DialogContent from "@material-ui/core/DialogContent";
import Autocomplete from "@material-ui/lab/Autocomplete";
import TextField from "@material-ui/core/TextField";
import DialogActions from "@material-ui/core/DialogActions";
import Button from "@material-ui/core/Button";
import SidePanel from "./SidePanel";

function CourseSelectionPopUp(props) {
    const [courses, setCourses] = useState([]);

    const handleChange = (event, newValue) => {
      setCourses(newValue);
    }

    return (
      <Dialog open={props.active} aria-labelledby="form-dialog-title" onClose={props.onClose}>
        <DialogTitle id="form-dialog-title" className="popup-title">Create a New Schedule</DialogTitle>
        <DialogContent>
          <Autocomplete
            multiple
            autoComplete
            filterSelectedOptions
            options={props.courseList}
            getOptionLabel={(option) => option.course_id + ' - ' + option.title}
            style={{width: 500}}
            renderInput={(params) => <TextField {...params} label='Course Search' />}
            onChange={handleChange}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => {props.onClose(); props.generateSchedules(courses)}}>
            Generate
          </Button>
        </DialogActions>
      </Dialog>
    );
  }

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
        <CourseSelectionPopUp
          active={this.state.showCourseSelection}
          courseList={this.props.courseList}
          generateSchedules={this.generateSchedules}
          onClose={() => this.setState({showCourseSelection: false})}
        />
        <SidePanel />
        <TimeGrid />
        <Button
          className='add-course-button'
          variant='contained'
          color='primary'
          onClick={() => this.setState({showCourseSelection: true})}
        >
          Add Courses
        </Button>
        <Button
          style={{paddingRight: '15px'}}
          className='add-course-button'
          onClick={() => {
            if (this.state.showSidePanel === false)
              document.getElementById('side-panel').style.marginLeft = '0vw';
            else
              document.getElementById('side-panel').style.marginLeft = '-31vw';
            this.setState({
              showSidePanel: !this.state.showSidePanel
            });
          }}
        >
          Toggle SidePanel
        </Button>
      </div>
    );
  }
}

export default ScheduleView;