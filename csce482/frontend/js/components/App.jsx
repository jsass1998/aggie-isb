import React, { Component } from 'react';
import TopBar from "./TopBar";
import TimeGrid from "./schedule/TimeGrid";

class App extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return(
            <div>
                <TopBar/>
                <TimeGrid/>
            </div>
        );
    }
}

export default App;