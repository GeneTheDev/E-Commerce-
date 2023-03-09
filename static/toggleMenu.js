let MenuItems = document.getElementById("MenuItems");

if (MenuItems) {
  MenuItems.style.maxHeight = "0px";

  function menuToggle() {
    if (MenuItems.style.maxHeight == "0px") {
      MenuItems.style.maxHeight = "200px";
    } else {
      MenuItems.style.maxHeight = "0px";
    }
  }
} else {
  console.log("Element with ID 'MenuItems' not found.");
}

// js for product gallery

window.onload = function () {
  let ProductImg = document.getElementById("ProductImg");
  let SmallImg = document.getElementsByClassName("small-img");

  if (SmallImg.length > 0) {
    SmallImg[0].onclick = function () {
      ProductImg.src = SmallImg[0].src;
    };
  }

  if (SmallImg.length > 1) {
    SmallImg[1].onclick = function () {
      ProductImg.src = SmallImg[1].src;
    };
  }

  if (SmallImg.length > 2) {
    SmallImg[2].onclick = function () {
      ProductImg.src = SmallImg[2].src;
    };
  }

  if (SmallImg.length > 3) {
    SmallImg[3].onclick = function () {
      ProductImg.src = SmallImg[3].src;
    };
  }
};
