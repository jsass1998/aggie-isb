import React, { useState } from 'react';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Button from "@material-ui/core/Button";
import Checkbox from "@material-ui/core/Checkbox";
import {
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
} from '@material-ui/core';

function PopUpDialog(props) {
  const [checked, setChecked] = useState(false);

  return (
    <Dialog open={props.active} aria-labelledby="form-dialog-title" onClose={props.onClose}>
      <DialogTitle id="form-dialog-title" className="popup-title">{props.title}</DialogTitle>
      <DialogContent>
        <div className="dialog-message-text">{props.message} </div>
      </DialogContent>
      <DialogActions>
        <FormGroup row>
          <FormControlLabel
            control={<Checkbox checked={checked} color='primary' onChange={() => { setChecked(!checked); props.handleCheckChanged()}} name='showAgain' />}
            label={'Don\'t show again'}
          />
          <Button onClick={props.onClose}>
            Close
          </Button>
        </FormGroup>
      </DialogActions>
    </Dialog>
  );
}

export default PopUpDialog;