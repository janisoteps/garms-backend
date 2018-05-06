import React from "react";
import {List, ListItem} from 'material-ui/List';
import ContentInbox from 'material-ui/svg-icons/content/inbox';
import FlatButton from 'material-ui/FlatButton';


export default class TestList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      tests: [
        {name: 'CNC Font Test', driver: 'FireFox'},
        {name: 'CNC Line Widget Test', driver: 'FireFox'},
        {name: 'CNC Widget Position Test', driver: 'FireFox'},
        {name: 'CNC Widget Scaling Test', driver: 'FireFox'},
        {name: 'CNC Widget Rotation Test', driver: 'FireFox'},
        {name: 'CNC Lightbox Test', driver: 'FireFox'}
      ]
    };
  }



  render () {
    const listItems = this.state.tests.map(function(testItem, index){
      let text = "Name: " + testItem.name + ", Selenium driver: " + testItem.driver;
      let key = index;
      // console.log(testItem);
      return(
        <ListItem key={key} primaryText={text} leftIcon={<ContentInbox />} rightIconButton={<FlatButton className="single-test-run-button" backgroundColor="#a4c639"
      hoverColor="#8AA62F" label="Run"/>}/>
      )
    });

    return (
      <List>
        {listItems}
      </List>
    )
  }
}
