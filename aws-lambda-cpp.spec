
%global gh_url https://github.com/awslabs/aws-lambda-cpp
Name: aws-lambda-cpp
Version: 0.2.8
%global gittag v%{version}

Release: 1%{?dist}
Summary: C++ implementation of the AWS Lambda runtime
License: Apache-2.0
URL:	 %{gh_url}
Source:  %{gh_url}/archive/%{gittag}/%{name}-%{version}.tar.gz
# Upstream, but past 0.2.8
Patch0:  0008-Add-building-and-packaging-a-demo-project-to-CI-and-.patch
BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: curl-devel

%description
C++ implementation of the lambda runtime API.

This package includes a shared library providing functionality to interact
with the Lambda runtime. This allows you to provide Lambda functions from
your C++ application with negligible cold-start overhead.

This library will build on more CPU architectures than AWS Lambda supports.
An application to be run on Lambda will need to be built for an architecture
that AWS Lambda supports.

%package devel
Summary: Development files and static library for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
Development files for a C++ implementation of the lambda runtime API.

This includes header files and cmake code to assist you in building your
C++ application for use in Lambda. The included packager script can help
to assemble a .zip file to upload as a custom Lambda runtime.

This library will build on more CPU architectures than AWS Lambda supports.
An application to be run on Lambda will need to be built for an architecture
that AWS Lambda supports.

%package demo
Summary: Demo example of AWS Lambda C++ function

%description demo
The examples/demo simple Lambda function implemented in C++.

Note that while packaged for all architectures, the built .zip is only usable
on AWS Lambda if it is built for an architecture that Lambda supports.

%files devel
%{_includedir}/aws/http/response.h
%{_includedir}/aws/lambda-runtime/*
%{_includedir}/aws/logging/logging.h
%{_libdir}/libaws-lambda-runtime.so
%doc README.md CONTRIBUTING.md
%{_libdir}/aws-lambda-runtime/

%files
%{_libdir}/libaws-lambda-runtime.so.*
%license LICENSE

%files demo
%doc examples/demo/CMakeLists.txt examples/demo/main.cpp

%prep
%autosetup -n %{name}-%{version} -p1

%build
%cmake
%cmake_build

%install
%cmake_install

%check
%ctest

# Now build the demo at a test of things...
# FIXME: how do we build the binary and ship it in the -demo package?
export aws_lambda_build=$PWD/%{_vpath_builddir}
%define _vpath_srcdir examples/demo
%define _vpath_builddir %{_vendor}-%{_target_os}-demo-build
%cmake -Daws-lambda-runtime_DIR=$aws_lambda_build
%cmake_build

%changelog
* Sat Sep 16 2023 Stewart Smith <trawets@amazon.com> - 0.2.8-1
- Initial packaging
