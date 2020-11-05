import React, {Component} from 'react';
import TopBar from "./TopBar";
import TimeGrid from "./schedule/TimeGrid";

class App extends Component {
  constructor(props) {
    super(props);
    const { hideToolTips } = this.fetchLocalStorage();
    this.state = {
      hideToolTips: hideToolTips,
    }
  }

  fetchLocalStorage() {
    return {
      hideToolTips: Boolean(parseInt(localStorage.getItem('hideToolTips'))),
    };
  }

  render() {
    return(
      <div>
        <TopBar/>
        <TimeGrid
          hideToolTips={this.state.hideToolTips}
        />
      </div>
    );
  }
}

export default App;