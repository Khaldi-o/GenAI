import { createSlice } from "@reduxjs/toolkit";

const postSlice = createSlice({
  name: "post",
  initialState: { postData: {} },
  reducers: {
    writeData(state, action) {
      const postdata = action.payload;
      state.postData = postdata;
    },
  },
});
export const postActions = postSlice.actions;
export default postSlice;
