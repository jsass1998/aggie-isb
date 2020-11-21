export const GOOGLE_CLIENT_ID = '627245330757-i02jh16q75ba38fldohh71d5euth1dp2.apps.googleusercontent.com';

// map from Date().getDay() to a 3-letter string compatible with the database
export const weekdayMap = {
    0: "sunday",
    1: "monday",
    2: "tuesday",
    3: "wednesday",
    4: "thursday",
    5: "friday",
    6: "saturday",
};

// map from db-compatible weekday string to a date used by the TimeGrid to plot new time blocks
export const dayToDateMap = {
    "sunday": "2019-03-03",
    "monday": "2019-03-04",
    "tuesday": "2019-03-05",
    "wednesday": "2019-03-06",
    "thursday": "2019-03-07",
    "friday": "2019-03-08",
    "saturday": "2019-03-09",
};

export const create_schedule_tooltip = 'This is where you can block out time for extracurriculars, work, ' +
  'studying, eating, or anything else you want to make sure you have time for in your day. Click and drag ' +
  'on the schedule to mark the times you are unavailable for class, then expand the side panel on the left ' +
  'to select the courses you want to register for and we’ll look for schedules that work for you! '

// Lorem ipsum - used for large placeholder text
export const lorem_ipsum = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec nec diam id libero ' +
  'ullamcorper ullamcorper. Suspendisse ut consequat nunc, non accumsan sem. Suspendisse potenti. Donec diam ' +
  'neque, pellentesque non accumsan eu, pulvinar eget libero. Curabitur ornare, tellus sit amet bibendum ' +
  'ullamcorper, justo lorem fermentum quam, sit amet fermentum sem odio a ante. Class aptent taciti sociosqu ' +
  'ad litora torquent per conubia nostra, per inceptos himenaeos. Nulla pellentesque metus nunc, nec posuere ' +
  'urna pharetra ac. Donec at mi semper, mattis lorem eu, hendrerit tellus.';