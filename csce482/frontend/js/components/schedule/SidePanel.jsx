import React, { Component } from 'react';
import { styled } from '@material-ui/core/styles';
import Grid from "@material-ui/core/Grid";
import Paper from "@material-ui/core/Paper";

const ColumnPaper = styled(Paper)({
  borderRadius: 3,
  textAlign: 'center',
});

class SidePanel extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div id='side-panel' className='aisb-card'>
        <Grid
          container
          spacing={1}
          justify='center'
          alignItems='stretch'
          style={{height: '100%'}}
        >
          <Grid item xs={8}>
            <div
              className='side-panel-column'
              style={{backgroundColor: '#A00000', color: 'white'}}
            >
              Column 1
            </div>
          </Grid>
          <Grid item xs={4}>
            <div
              className='side-panel-column'
              style={{backgroundColor: '#500000', color: 'white'}}
            >
              Column 2
            </div>
          </Grid>
        </Grid>
      </div>
    );
  }
}

export default SidePanel;