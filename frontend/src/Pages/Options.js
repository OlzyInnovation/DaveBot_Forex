import React, { useEffect, useState } from "react";
import * as html2canvas from "html2canvas";

function canvas() {
  html2canvas(document.querySelector("#capture")).then((canvas) => {
    // document.body.appendChild(canvas);
    const dataURL = canvas.toDataURL();
    console.log("Canvas URL:", dataURL);
  });
}

function Options() {
  //   const [data, setData] = useState([]);
  useEffect(() => {
    const el = document.querySelector("#capture");
    // setInterval(canvas, 5000);
    // setInterval(function () {
    //   html2canvas(el).then((canvas) => {
    //     // document.body.appendChild(canvas);
    //     const dataURL = canvas.toDataURL();
    //     console.log("Canvas URL:", dataURL);
    //   });
    // }, 5000);
    // console.log("El :", el);
    // html2canvas(el).then((canvas) => {
    //   const dataURL = canvas.toDataURL();
    //   console.log("Canvas URL:", dataURL);
    //   // document.body.appendChild(canvas);
    //   // console.log("Canvas :", canvas);
    // });
  }, []);

  return (
    <>
      <div id="capture">
        <h4>Hello world!</h4>
      </div>
    </>
  );
}

export default Options;
