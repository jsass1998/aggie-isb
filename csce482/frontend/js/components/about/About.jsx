import React, { Component } from 'react';
import {routeCodes} from "../../config/routes";

class About extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return(
            <div>
                <h1>About page coming soon!</h1>
                <button onClick={() => this.props.history.push(routeCodes.HOME)}>
                    HOME
                </button>
            </div>
        );
    }
}

export default About;