import { createSlice } from "@reduxjs/toolkit";

const previewSlice = createSlice({
  name: "preview",
  initialState: { previewData: {}, openPreview: false, save:false },
  reducers: {
    writeData(state, action) {
      const previewdata = action.payload;
      console.log('payload', { ...state.previewData, ...previewdata });
      state.previewData = { ...state.previewData, ...previewdata };
    },
    openPreview(state) {
      state.openPreview = true;
    },
    save(state) {
      state.save = true;
    },
    closePreview(state) {
      console.log('state',state);
      state.previewData = {};
      state.openPreview = false;
      state.save = true;
    },
    editText(state, action) {
      const text = action.payload;
      state.previewData.text = text;
    },
    editImageText(state, action) {
      const text = action.payload;
      state.previewData.image_prompt = text;
    },
  },
});
export const previewActions = previewSlice.actions;
export default previewSlice;
