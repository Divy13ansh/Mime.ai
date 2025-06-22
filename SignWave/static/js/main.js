import * as THREE from 'https://cdn.skypack.dev/three@0.132.2';

var label = document.getElementById("label");
var container = document.getElementById("container");

const fov = 75;
const aspect = container.clientWidth / container.clientHeight;
const near = 0.1;
const far = 1000;

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x253238);
const camera = new THREE.PerspectiveCamera(fov, aspect, near, far);

const renderer = new THREE.WebGLRenderer();
renderer.setSize(container.clientWidth, container.clientHeight);
container.appendChild(renderer.domElement);

var wordList = [];
var wordidx = 0;
var frameidx = 0;

var textForm = document.getElementById("inputForm");
textForm.addEventListener("submit", function (e) {
    e.preventDefault();
    var message = document.getElementById("message").value;
    wordList = message.trim().split(" ");
    frameidx = 0;
    wordidx = 0;
    console.log(wordList);
});

fetch('static/json/reference1_normalized.json')
    .then(response => response.json())
    .then(data => {
        function drawPoint(x, y, z) {
            const pointRadius = 0.25;
            const geometry = new THREE.SphereGeometry(pointRadius, 32, 16);
            const material = new THREE.MeshBasicMaterial({ color: 0x84FFFF });
            const sphere = new THREE.Mesh(geometry, material);
            scene.add(sphere);
            sphere.position.set(x, y, z);
        }

        function drawLine(x1, y1, z1, x2, y2, z2) {
            const points = [new THREE.Vector3(x1, y1, z1), new THREE.Vector3(x2, y2, z2)];
            const geometry = new THREE.BufferGeometry().setFromPoints(points);
            const material = new THREE.LineBasicMaterial({ color: 0xFFFFFF });
            const line = new THREE.Line(geometry, material);
            scene.add(line);
        }

        function redistributeElements(left, right) {
            if (left.length > 21) {
                const redistributedElements = left.splice(21);
                right.push(...redistributedElements);
            } else if (right.length > 21) {
                const redistributedElements = right.splice(21);
                left.push(...redistributedElements);
            }
        }

        function connectLines(left, right) {
            const edgeList = [[0, 1], [1, 2], [2, 3], [3, 4], [0, 5], [5, 6], [6, 7], [7, 8], [5, 9], [9, 10], [10, 11], [11, 12], [9, 13], [13, 14], [14, 15], [15, 16], [13, 17], [17, 18], [18, 19], [19, 20], [0, 17]];
            redistributeElements(left, right);

            edgeList.forEach(edge => {
                const [u, v] = edge;
                if (left[u] && left[v]) {
                    const l1 = left[u]['Coordinates'];
                    const l2 = left[v]['Coordinates'];
                    drawLine(l1[0] * 50, l1[1] * -50, l1[2] * 50, l2[0] * 50, l2[1] * -50, l2[2] * 50);
                }
                if (right[u] && right[v]) {
                    const r1 = right[u]['Coordinates'];
                    const r2 = right[v]['Coordinates'];
                    drawLine(r1[0] * 50, r1[1] * -50, r1[2] * 50, r2[0] * 50, r2[1] * -50, r2[2] * 50);
                }
            });
        }

        let clock = new THREE.Clock();
        let delta = 0;
        let interval = 1 / 10;

        function render() {
            requestAnimationFrame(render);
            delta += clock.getDelta();

            if (delta > interval) {
                delta = delta % interval;

                if (wordidx < wordList.length) {
                    const currentWord = wordList[wordidx];
                    const frames = data[currentWord];

                    if (!frames) {
                        console.warn("No data for word:", currentWord);
                        wordidx++;
                        frameidx = 0;
                        return;
                    }

                    const frame = frames.find(f => f.Frame === frameidx);

                    if (!frame) {
                        wordidx++;
                        frameidx = 0;
                        return;
                    }

                    const left = frame["Left Hand Coordinates"] || [];
                    const right = frame["Right Hand Coordinates"] || [];

                    label.innerHTML = currentWord.toUpperCase();

                    left.forEach(joint => {
                        const [x, y, z] = joint['Coordinates'];
                        drawPoint(x * 50, y * -50, z * 50);
                    });

                    right.forEach(joint => {
                        const [x, y, z] = joint['Coordinates'];
                        drawPoint(x * 50, y * -50, z * 50);
                    });

                    connectLines(left, right);

                    frameidx++;
                    if (frameidx >= frames.length) {
                        wordidx++;
                        frameidx = 0;
                    }
                } else {
                    label.innerHTML = "N/A";
                }

                renderer.render(scene, camera);
                scene.remove(...scene.children);
            }
        }

        render();
    });

camera.position.set(27.5, -30, 25);
