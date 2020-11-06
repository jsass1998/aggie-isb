import React, {Component} from 'react';
import axios from 'axios';
import TopBar from "./TopBar";
import TimeGrid from "./schedule/TimeGrid";
import CircularProgress from "@material-ui/core/CircularProgress";
import ScheduleView from "./schedule/ScheduleView";

/*
  * <App/> is the root component for the schedule view page and will consist of the most
  * logic and complexity as it is where the user is expected to spend the majority of their
  * time interacting with the site.
 */

class App extends Component {
  constructor(props) {
    super(props);
    const { hideToolTips } = this.fetchLocalStorage();
    this.state = {
      hideToolTips: hideToolTips,
      courseList: [],
    }
  }

  componentDidMount() {
    this.fetchCourseData().then(r => {});
  }

  fetchLocalStorage() {
    return {
      hideToolTips: Boolean(parseInt(localStorage.getItem('hideToolTips'))),
    };
  }

  async fetchCourseData() {
    let res = await axios.get('api/courses/');
    this.setState({
      courseList: res.data,
    });
  }

  render() {
    if (!this.state.courseList)
      return (
        <div>
          <TopBar/>
          <div className={'loading-wheel'}>
            <CircularProgress />
            <div>Loading...</div>
          </div>
        </div>
      );
    return(
      <div>
        <TopBar/>
        <ScheduleView
          hideToolTips={this.state.hideToolTips}
          courseList={this.state.courseList}
        />
      </div>
    );
  }
}

export default App;