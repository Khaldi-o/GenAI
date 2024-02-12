import { createSlice } from "@reduxjs/toolkit";

const previewSlice = createSlice({
  name: "preview",
  initialState: { previewData: {}, openPreview: false },
  reducers: {
    writeData(state, action) {
      const previewdata = action.payload;
      state.previewData = { ...state.previewData, ...previewdata };
    },
    openPreview(state) {
      state.openPreview = true;
    },
    closePreview(state) {
      state.previewData = {};
      state.openPreview = false;
    },
    editText(state, action) {
      const text = action.payload;
      state.previewData.text = text;
    },
  },
});
export const previewActions = previewSlice.actions;
export default previewSlice;
