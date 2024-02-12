import { useDispatch } from "react-redux";
import { previewActions } from "../store/preview-slice";
import Button from "./UI/Button";

export default function ImageSnippet({ image }) {
  const dispatch = useDispatch();

  const handlePreview = () => {
    dispatch(
      previewActions.writeData({
        id: image.id,
        url: image.url,
      }),
    );
    dispatch(previewActions.openPreview());
  };
  return (
    <div className="flex flex-col items-center justify-center">
      <img
        src={image.url}
        alt={`number ${image.id}`}
        className="w-full h-auto"
      />
      <Button onClick={handlePreview}> Preview </Button>
    </div>
  );
}
