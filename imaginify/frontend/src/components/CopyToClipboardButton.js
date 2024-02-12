function CopyToClipboardButton({ textToCopy, children }) {
  const handleCopy = () => {
    navigator.clipboard
      .writeText(textToCopy)
      .then(() => {
        // Handle successful copying here, like showing a notification
        alert("Text copied to clipboard!");
      })
      .catch((err) => {
        // Handle errors here, like user denying clipboard permissions
        console.error("Could not copy text: ", err);
      });
  };

  return (
    <button
      className="mr-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-700 transition duration-300"
      onClick={handleCopy}
    >
      {children}
    </button>
  );
}

export default CopyToClipboardButton;
