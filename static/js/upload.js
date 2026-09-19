const fileInput = document.getElementById("fileInput");
const fileName = document.getElementById("fileName");
const form = document.getElementById("submissionForm");
const message = document.getElementById("formMessage");
const button = document.getElementById("submitBtn");

fileInput?.addEventListener("change", () => {
    fileName.textContent = fileInput.files?.[0]?.name || "هنوز فایلی انتخاب نشده است";
});

form?.addEventListener("submit", async (event) => {
    event.preventDefault();
    message.textContent = "";
    button.disabled = true;
    button.textContent = "در حال ارسال...";

    try {
        const response = await fetch("/api/submissions", {
            method: "POST",
            body: new FormData(form)
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.detail || "خطایی رخ داد.");
        message.textContent = data.message;
        message.style.color = "var(--teal)";
        form.reset();
        fileName.textContent = "هنوز فایلی انتخاب نشده است";
        window.showToast("اثر شما با موفقیت ثبت شد.");
    } catch (error) {
        message.textContent = error.message;
        message.style.color = "#d9534f";
    } finally {
        button.disabled = false;
        button.textContent = "ثبت و ارسال اثر";
    }
});
