import PageContent from "../components/PageContent";
import { useRouteLoaderData, Link } from "react-router-dom";
import Button from "../components/UI/Button";

function HomePage() {
  const token = useRouteLoaderData("root");

  return (
    <PageContent>
      <h1 className="mt-24 font-bold align-middle text-center text-6xl text-stone-100">
        {" "}
        Imaginify{" "}
      </h1>
      <h2 className="my-16 align-middle text-2xl text-stone-50 uppercase mx-auto w-1/2 text-center">
        {" "}
        Unlock your creativity: Instantly Generate Stunning Text and Visual
        Contents.
      </h2>
      {token && (
        <div className="flex justify-center">
          <Link to="/new" className="my-16">
            <Button>New post</Button>
          </Link>
        </div>
      )}
    </PageContent>
  );
}

export default HomePage;
