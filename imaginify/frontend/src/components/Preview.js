import Modal from "./UI/Modal";
import LinkedInPostLayout from "./UI/LinkedInPostLayout";

export default function Preview({ open, ...props }) {
  return (
    <Modal open={open} className="rounded">
      <LinkedInPostLayout />
    </Modal>
  );
}
