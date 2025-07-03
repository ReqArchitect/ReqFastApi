import { createStore } from 'redux';

const initialState = {
  modelTree: [],
  details: {},
};

function rootReducer(state = initialState, action) {
  switch (action.type) {
    case 'SET_MODEL_TREE':
      return { ...state, modelTree: action.payload };
    case 'SET_DETAILS':
      return { ...state, details: { ...state.details, ...action.payload } };
    default:
      return state;
  }
}

const store = createStore(rootReducer);
export default store;
