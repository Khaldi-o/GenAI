import ImageSnippet from "./ImageSnippet";

export default function ImageGrid({ images, ...props }) {
  return (
    <div className="container mx-auto p-4">
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 gap-4">
        {images &&
          images.map((image) => <ImageSnippet key={image.id} image={image} />)}
      </div>
    </div>
  );
}
