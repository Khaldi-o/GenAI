import NewPostForm from "../components/NewPostForm";
import NoCredit from "../components/NoCredit";
import { getCredits } from "../util/credit";

function NewPostPage() {
  const [text_credit] = getCredits();
  const credit = text_credit > 0;
  return <>{credit ? <NewPostForm method="post" /> : <NoCredit />}</>;
}

export default NewPostPage;
