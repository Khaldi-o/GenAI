import { RouterProvider, createBrowserRouter } from "react-router-dom";
import { Provider } from "react-redux";
import ErrorPage from "./pages/Error";
import HomePage from "./pages/Home";
import NewPostPage from "./pages/NewPost";
import RootLayout from "./pages/Root";
import { action as newPostAction } from "./components/NewPostForm";
import AuthenticationPage, {
  action as authAction,
} from "./pages/Authentication";
import { action as actionLogout } from "./pages/Logout";
import { tokenLoader, checkAuthLoader } from "./util/auth";
import PostPage, { action as actionPostOnNetwork } from "./pages/Post";
import HistoryPage, { loader as loaderHistory } from "./pages/History";
import store from "./store/index";

const router = createBrowserRouter([
  {
    path: "/",
    element: <RootLayout />,
    errorElement: <ErrorPage />,
    id: "root",
    loader: tokenLoader,
    children: [
      { index: true, element: <HomePage /> },
      {
        path: "auth",
        element: <AuthenticationPage />,
        action: authAction,
      },
      {
        path: "new",
        element: <NewPostPage />,
        action: newPostAction,
        loader: checkAuthLoader,
      },
      {
        path: "post",
        element: <PostPage />,
        action: actionPostOnNetwork,
        loader: checkAuthLoader,
      },
      {
        path: "history/:userId",
        element: <HistoryPage />,
        loader: loaderHistory,
      },
      {
        path: "logout",
        action: actionLogout,
      },
    ],
  },
]);

function App() {
  return (
    <Provider store={store}>
      <RouterProvider router={router} />
    </Provider>
  );
}

export default App;
