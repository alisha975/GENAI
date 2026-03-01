import os
import sys
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from fastapi.staticfiles import StaticFiles
from starlette.routing import Route

# Add the src directory to sys.path to allow imports from agent
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "../src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from agent.app import app, create_frontend_router

class TestApp:
    def test_create_frontend_router_success(self):
        """
        Test that StaticFiles is returned when the build directory and index.html exist.
        """
        with patch("agent.app.pathlib.Path") as mock_path_cls, \
             patch("agent.app.StaticFiles") as mock_static_files:
            # Create a mock path object that will be returned by Path(...) and its operations
            mock_path_obj = MagicMock()
            mock_path_cls.return_value = mock_path_obj
            
            # Ensure chaining operations return the same mock object or a compatible one
            mock_path_obj.parent = mock_path_obj
            mock_path_obj.__truediv__.return_value = mock_path_obj
            
            # Set expectations for success: directory exists and file exists
            mock_path_obj.is_dir.return_value = True
            mock_path_obj.is_file.return_value = True
            
            router = create_frontend_router()
            
            # Verify that the router returned is the mock instance from StaticFiles
            assert router == mock_static_files.return_value

    def test_create_frontend_router_missing_dir(self):
        """
        Test that a dummy Route is returned when the build directory does not exist.
        """
        with patch("agent.app.pathlib.Path") as mock_path_cls:
            mock_path_obj = MagicMock()
            mock_path_cls.return_value = mock_path_obj
            
            mock_path_obj.parent = mock_path_obj
            mock_path_obj.__truediv__.return_value = mock_path_obj
            
            # Set expectation: directory does not exist
            mock_path_obj.is_dir.return_value = False
            
            router = create_frontend_router()
            
            assert isinstance(router, Route)

    def test_create_frontend_router_missing_index(self):
        """
        Test that a dummy Route is returned when the directory exists but index.html is missing.
        """
        with patch("agent.app.pathlib.Path") as mock_path_cls:
            mock_path_obj = MagicMock()
            mock_path_cls.return_value = mock_path_obj
            
            mock_path_obj.parent = mock_path_obj
            mock_path_obj.__truediv__.return_value = mock_path_obj
            
            # Set expectation: directory exists but file does not
            mock_path_obj.is_dir.return_value = True
            mock_path_obj.is_file.return_value = False
            
            router = create_frontend_router()
            
            assert isinstance(router, Route)

    def test_dummy_frontend_response(self):
        """
        Test that the dummy frontend route returns a 503 status code and correct message.
        """
        # Force the router to be the dummy one
        with patch("agent.app.pathlib.Path") as mock_path_cls:
            mock_path_obj = MagicMock()
            mock_path_cls.return_value = mock_path_obj
            mock_path_obj.parent = mock_path_obj
            mock_path_obj.__truediv__.return_value = mock_path_obj
            mock_path_obj.is_dir.return_value = False
            
            router = create_frontend_router()
            
            # Create a temporary FastAPI app to mount the router
            from fastapi import FastAPI
            test_app = FastAPI()
            test_app.mount("/", router)
            
            client = TestClient(test_app)
            response = client.get("/some/path")
            
            assert response.status_code == 503
            assert "Frontend not built" in response.text

    def test_app_mounts(self):
        """
        Smoke test to ensure the main app object is created and has the frontend mounted.
        """
        # Check if 'frontend' route is mounted
        routes = [route for route in app.routes if getattr(route, "name", None) == "frontend"]
        assert len(routes) > 0