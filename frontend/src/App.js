import {AppBar, Button, CircularProgress, Grid, ImageList, ImageListItem, Toolbar, Typography} from "@mui/material";
import "./App.css"
import {useRef, useState} from "react";
import axios from "axios";

function App() {
    const [loading, setLoading] = useState(false);
    const [images, setImages] = useState([]);
    const [filesContent, setFilesContent] = useState([]);

    const hiddenFileInput = useRef(null);

    const openFileSelector = event => {
        hiddenFileInput.current.click();
    };

    const handleChange = event => {
        setFilesContent(event.target.files);

        setLoading(true);

        const formData = new FormData();
        formData.append("file", event.target.files[0]);

        axios.post("http://redmoon-pc.local:9002/api/v1/mnist/predict", formData, {
            headers: {
                "Content-Type": "multipart/form-data",
            }
        })
            .then(response => response.data)
            .then(imgs => setImages(imgs))
            .then(() => setLoading(false));
    };

    return (<Grid direction="column" style={{height: "100vh"}}>
        <Grid item>
            <AppBar position="static">
                <Toolbar>
                    <Typography
                        variant="h6"
                        component="div"
                    >
                        MNIST Reverse Image Search
                    </Typography>
                </Toolbar>
            </AppBar>
        </Grid>
        <Grid item style={{height: "calc(100vh - 64px)", width: "100%"}}>
            <Grid container
                  direction="column"
                  justifyContent="center"
                  alignItems="center"
                  style={{height: "100%", width: "100%"}}
            >
                <Grid item style={{width: "500px", marginBottom: "20px"}}>
                    <Button variant="outlined" fullWidth onClick={() => openFileSelector()}>
                        {loading ? <CircularProgress
                            size={24}/> : (filesContent.length > 0 ? filesContent[0].name : "Choose a file")}
                    </Button>
                    <input
                        type="file"
                        ref={hiddenFileInput}
                        onChange={handleChange}
                        style={{display: 'none'}}
                    />
                </Grid>
                <Grid item style={{width: "500px"}}>
                    {images.length > 0 && <ImageList sx={{width: 500, height: 450}} cols={3} rowHeight={164}>
                        {images.map((item, i) => (<ImageListItem key={i}>
                            <img
                                src={`data:image/png;base64, ${item}`}
                                loading="lazy"
                            />
                        </ImageListItem>))}
                    </ImageList>}
                </Grid>
            </Grid>
        </Grid>
    </Grid>);
}

export default App;
