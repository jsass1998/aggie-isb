import React, { Component } from 'react';

class TopBar extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return(
            <div className='aisb-topbar aisb-card'>
                <h1>Aggie ISB</h1>
                {/* TODO: WIP - Finish user acct / sign in component */}
                {/*<div id='sign-in'>*/}
                {/*    <p>Sign in</p>*/}
                {/*    <span class='dot'></span>*/}
                {/*</div>*/}
            </div>
        );
    }
}

export default TopBar;