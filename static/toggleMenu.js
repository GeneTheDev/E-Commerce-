let MenuItems = document.getElementById("MenuItems");

MenuItems.style.maxHeight = "0px";

function menuToggle() {
  if (MenuItems.style.maxHeight == "0px") {
    MenuItems.style.maxHeight = "200px";
  } else {
    MenuItems.style.maxHeight = "0px";
  }
}

// js for product gallery

window.onload = function () {
  let ProductImg = document.getElementById("ProductImg");
  let SmallImg = document.getElementsByClassName("small-img");

  SmallImg[0].onClick = function () {
    ProductImg.src = SmallImg[0].src;
  };
  SmallImg[1].onClick = function () {
    ProductImg.src = SmallImg[1].src;
  };
  SmallImg[2].onClick = function () {
    ProductImg.src = SmallImg[2].src;
  };
  SmallImg[3].onClick = function () {
    ProductImg.src = SmallImg[3].src;
  };
};
