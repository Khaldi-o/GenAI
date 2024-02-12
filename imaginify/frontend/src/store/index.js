import { configureStore } from "@reduxjs/toolkit";
import postSlice from "./post-slice";
import previewSlice from "./preview-slice";

const store = configureStore({
  reducer: { post: postSlice.reducer, preview: previewSlice.reducer },
});

export default store;
