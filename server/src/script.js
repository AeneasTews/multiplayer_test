const url = window.location.href;

function set_status(status) {
  const element = document.getElementById("status");
  element.innerText = `Status: ${status}`;
}

async function sha_256(string) {
  const utf8 = new TextEncoder().encode(string);
  return crypto.subtle.digest('SHA-256', utf8).then((hashBuffer) => {
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    // convert to hex
    return hashArray
        .map((bytes) => bytes.toString(16).padStart(2, '0'))
        .join('');
  });
}

async function hash_data(id_list) {
  let hash_string = "";

  id_list.forEach((id) => {
    hash_string += document.getElementById(id).value;
  });

  return await sha_256(hash_string);
}

async function send_create_request(username, passwd_hash) {
  const req = new Request(`${url}create_user`);

  const req_data = JSON.stringify({
    "username": username,
    "passwd_hash": passwd_hash,
  });

  return await fetch(req, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: req_data,
  });
}

async function create_user() {
  // get data
  const username = document.getElementById("uname").value;
  const passwd_hash = await hash_data(["passwd"])

  // send request and handle response
  const res = await send_create_request(username, passwd_hash);
  const res_data = await res.json();

  set_status(res_data.status);
}

async function setup() {
  const submit_button = document.getElementById("submit");
  submit_button.addEventListener("click", async () => {
    await create_user();
  });
}

setup();